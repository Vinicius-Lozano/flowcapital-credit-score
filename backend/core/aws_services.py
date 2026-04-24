import json
import uuid

import boto3
from django.conf import settings


def _cliente(servico):
    return boto3.client(
        servico,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_DEFAULT_REGION,
    )


# ── S3 ───────────────────────────────────────────────────────────────────────

def upload_s3(bytes_arquivo, nome_arquivo, content_type='application/pdf'):
    chave = f'extratos/{nome_arquivo}'
    _cliente('s3').put_object(
        Bucket=settings.AWS_S3_BUCKET_NAME,
        Key=chave,
        Body=bytes_arquivo,
        ContentType=content_type,
    )
    return chave


# ── Textract ─────────────────────────────────────────────────────────────────

def extrair_texto_pdf(bytes_pdf):
    resposta = _cliente('textract').detect_document_text(Document={'Bytes': bytes_pdf})
    linhas = [
        bloco['Text']
        for bloco in resposta['Blocks']
        if bloco['BlockType'] == 'LINE'
    ]
    return '\n'.join(linhas)


# ── Bedrock ───────────────────────────────────────────────────────────────────

_MODEL_ID = 'anthropic.claude-3-haiku-20240307-v1:0'


def _invocar_bedrock(prompt, max_tokens=600):
    payload = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': max_tokens,
        'messages': [{'role': 'user', 'content': prompt}],
    }
    resposta = _cliente('bedrock-runtime').invoke_model(
        modelId=_MODEL_ID,
        body=json.dumps(payload),
        contentType='application/json',
        accept='application/json',
    )
    resultado = json.loads(resposta['body'].read())
    return resultado['content'][0]['text']


def extrair_transacoes_via_ia(texto_extrato):
    """Envia o texto bruto do extrato ao Bedrock e recebe transações estruturadas."""
    prompt = f"""Você é um sistema de processamento de extratos bancários.
Analise o texto abaixo e retorne APENAS um JSON válido, sem nenhum texto adicional.
Formato esperado:

[
  {{"data": "YYYY-MM-DD", "tipo": "PIX_RECEBIDO", "valor": 150.00, "descricao": "Descrição"}},
  {{"data": "YYYY-MM-DD", "tipo": "BOLETO_PAGO", "valor": 80.00, "descricao": "Descrição"}}
]

Tipos válidos: PIX_RECEBIDO, TED_RECEBIDO, BOLETO_PAGO, COMPRA_CARTAO, TARIFA_BANCARIA, TED_ENVIADO.
Use PIX_RECEBIDO ou TED_RECEBIDO para qualquer entrada de dinheiro.
Retorne SOMENTE o JSON, sem markdown, sem explicações.

Texto do extrato:
{texto_extrato}"""

    texto = _invocar_bedrock(prompt, max_tokens=2000).strip()

    # remove blocos markdown se Claude retornar com ```json
    if texto.startswith('```'):
        linhas = texto.split('\n')
        texto = '\n'.join(linhas[1:-1]).strip()

    return json.loads(texto)


def gerar_analise_credito_ia(transacoes, score, renda, despesa):
    """Gera um parecer narrativo da análise de crédito via Claude 3 Haiku."""
    n_entradas = sum(1 for t in transacoes if t.get('tipo') in ('PIX_RECEBIDO', 'TED_RECEBIDO'))
    n_saidas = len(transacoes) - n_entradas

    prompt = f"""Você é um analista de crédito especializado em trabalhadores de renda variável.
Escreva um parecer profissional e objetivo em português, em 3 a 4 frases corridas (sem bullet points).
Mencione o perfil financeiro, pontos positivos e uma recomendação clara.

Dados do cliente:
- Score: {score}/1000
- Receita total: R$ {renda:.2f}
- Despesa total: R$ {despesa:.2f}
- Saldo líquido: R$ {(renda - despesa):.2f}
- Transações de entrada: {n_entradas}
- Transações de saída: {n_saidas}"""

    return _invocar_bedrock(prompt, max_tokens=400)


