import random
import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .pluggy_service import generate_connect_token, fetch_transactions
from . import aws_services

def fetch_mock_transactions(user):
    """
    Gera transações simuladas de forma determinística pelo CPF + mês.
    Simula o perfil de um trabalhador de renda variável (ex: motorista de app).
    """
    hoje = date.today()
    random.seed(f"{user.cpf}_{hoje.month}_{hoje.year}")

    transacoes = []

    for _ in range(random.randint(20, 80)):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': 'PIX_RECEBIDO',
            'valor': round(random.uniform(5, 200), 2),
            'descricao': 'Recebimento de Corridas (App)',
        })

    for _ in range(random.randint(2, 6)):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': random.choice(['BOLETO_PAGO', 'COMPRA_CARTAO']),
            'valor': round(random.uniform(100, 3000), 2),
            'descricao': 'Despesa',
        })

    random.seed()
    return transacoes

def _calcular_score(transacoes):
    renda = 0.0
    despesa = 0.0

    for t in transacoes:
        tipo = t.get('tipo')
        valor = float(t.get('valor', 0))
        if tipo in ('PIX_RECEBIDO', 'TED_RECEBIDO'):
            renda += valor
        elif tipo in ('BOLETO_PAGO', 'COMPRA_CARTAO', 'TARIFA_BANCARIA', 'TED_ENVIADO'):
            despesa += valor

    score = 300
    if renda > despesa * 1.5:
        score += 450
    elif renda > despesa:
        score += 250
    else:
        score -= 100

    score = max(0, min(1000, int(score)))

    if score >= 700:
        status_credito, cor = 'Crédito Aprovado!', 'green'
    elif score >= 500:
        status_credito, cor = 'Microcrédito Aprovado', 'orange'
    else:
        status_credito, cor = 'Crédito Negado', 'red'

    return score, status_credito, cor, renda, despesa

# ── Endpoints ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def pluggy_token(request):
    """Gera o token de conexão para o Widget Pluggy"""
    try:
        token = generate_connect_token(client_user_id=request.user.cpf)
        if token:
            return Response({"accessToken": token})
        return Response(
            {"error": "Erro ao autenticar com Pluggy. Verifique o CLIENT_ID/SECRET no .env"},
            status=503
        )
    except Exception as e:
        return Response(
            {"error": f"Erro interno ao comunicar com Pluggy: {str(e)}"},
            status=500
        )

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def analisar_credito(request):
    """
    Analisa dados da Pluggy ou Simulation com IA AWS.
    """
    user = request.user
    item_id = request.data.get("item_id")
    is_mock = request.data.get("mock", False)
    
    origem = "Simulação (Mock)"
    transacoes = []

    if is_mock:
        transacoes = fetch_mock_transactions(user)
    elif item_id:
        transacoes_pluggy = fetch_transactions(item_id)
        # Mapeia formato Pluggy para o nosso formato interno.
        # Pluggy: amount is always positive; type is 'CREDIT' or 'DEBIT'.
        for t in transacoes_pluggy:
            tipo_pluggy = t.get('type', 'DEBIT')
            is_credito = tipo_pluggy == 'CREDIT'
            transacoes.append({
                'data': t.get('date'),
                'tipo': 'PIX_RECEBIDO' if is_credito else 'COMPRA_CARTAO',
                'valor': abs(float(t.get('amount', 0))),
                'descricao': t.get('description') or t.get('name', '')
            })
        origem = "Pluggy"
    else:
        # Failsafe automático
        transacoes = fetch_mock_transactions(user)

    score, status_credito, cor, renda, despesa = _calcular_score(transacoes)

    analise_ia = ''
    try:
        analise_ia = aws_services.gerar_analise_credito_ia(transacoes, score, renda, despesa)
    except Exception as e:
        print(f'[Bedrock] indisponível: {e}')

    return Response({
        'score': score,
        'status': status_credito,
        'cor': cor,
        'origem': origem,
        'analise_ia': analise_ia,
        'detalhes': {
            'renda_calculada': f'R$ {renda:.2f}',
            'despesa_calculada': f'R$ {despesa:.2f}',
            'qtd_transacoes_analisadas': len(transacoes),
        },
        'transacoes': transacoes,
    })

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def pluggy_webhook(request):
    """
    Endpoint para receber notificações em tempo real da Pluggy.
    Documentação: https://docs.pluggy.ai/docs/webhooks
    """
    event = request.data
    event_type = event.get('event')
    item_id = event.get('itemId')
    
    print(f"Recebido Webhook Pluggy: {event_type} | Item ID: {item_id}")
    
    if event_type == 'item/created':
        pass
    elif event_type == 'item/updated':
        pass
    elif event_type == 'item/error':
        error_detail = event.get('error')
        print(f"Erro no item {item_id}: {error_detail}")

    return Response({"received": True}, status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_extrato_pdf(request):
    """
    Recebe um PDF de extrato bancário, sobe no S3, extrai texto via Textract
    e usa o Bedrock para transformar o texto em transações estruturadas.
    Retorna análise completa de crédito.
    """
    arquivo = request.FILES.get('pdf')
    if not arquivo:
        return Response({'erro': 'Envie o arquivo PDF no campo "pdf".'}, status=400)

    bytes_pdf = arquivo.read()
    nome_arquivo = f'{uuid.uuid4().hex}.pdf'

    try:
        chave_s3 = aws_services.upload_s3(bytes_pdf, nome_arquivo)
    except Exception as e:
        return Response({'erro': f'Falha ao salvar PDF no S3: {e}'}, status=500)

    try:
        texto_extrato = aws_services.extrair_texto_pdf(bytes_pdf)
    except Exception as e:
        return Response({'erro': f'Falha ao extrair texto com Textract: {e}'}, status=500)

    try:
        transacoes = aws_services.extrair_transacoes_via_ia(texto_extrato)
    except Exception as e:
        return Response({'erro': f'Falha ao estruturar transações com IA: {e}'}, status=500)

    score, status_credito, cor, renda, despesa = _calcular_score(transacoes)

    analise_ia = ''
    try:
        analise_ia = aws_services.gerar_analise_credito_ia(transacoes, score, renda, despesa)
    except Exception as e:
        print(f'[Bedrock] análise indisponível: {e}')

    return Response({
        'score': score,
        'status': status_credito,
        'cor': cor,
        'analise_ia': analise_ia,
        'arquivo_s3': chave_s3,
        'detalhes': {
            'renda_calculada': f'R$ {renda:.2f}',
            'despesa_calculada': f'R$ {despesa:.2f}',
            'qtd_transacoes_analisadas': len(transacoes),
        },
        'transacoes': transacoes,
    })
