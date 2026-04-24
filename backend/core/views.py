from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def analisar_credito(request):
    dados = request.data
    
    # Pega a lista de transações que veio do Quasar (se não vier, usa lista vazia)
    transacoes = dados.get('transacoes', [])
    
    renda_total = 0.0
    despesa_total = 0.0
    
    # O Motor Lendo o Extrato
    for transacao in transacoes:
        tipo = transacao.get('tipo')
        valor = float(transacao.get('valor', 0))
        
        if tipo == 'PIX_RECEBIDO':
            renda_total += valor
        elif tipo in ['BOLETO_PAGO', 'COMPRA_CARTAO', 'TARIFA_BANCARIA']:
            despesa_total += valor

    # Algoritmo de Score Base
    score = 300 
    
    if renda_total > (despesa_total * 1.5):
        score += 450  # Excelente pagador
    elif renda_total > despesa_total:
        score += 250  # Saudável
    else:
        score -= 100  # Risco de calote
        
    # Travas de limite (0 a 1000)
    score_final = max(0, min(1000, int(score)))

    # Decisão
    if score_final >= 700:
        status = "Crédito Aprovado!"
        cor = "positive"
    elif score_final >= 500:
        status = "Microcrédito Aprovado"
        cor = "warning"
    else:
        status = "Crédito Negado"
        cor = "negative"

    return Response({
        "score": score_final,
        "status": status,
        "cor": cor,
        "detalhes": {
            "renda_calculada": f"R$ {renda_total:.2f}",
            "despesa_calculada": f"R$ {despesa_total:.2f}",
            "qtd_transacoes_analisadas": len(transacoes)
        }
    })