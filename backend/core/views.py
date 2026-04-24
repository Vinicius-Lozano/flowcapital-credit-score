import random
from datetime import date
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

def fetch_belvo_transactions(user):
    """
    Mock integration for Belvo Sandbox API.
    Generates a deterministic simulation based on the user's CPF and the current month.
    """
    hoje = date.today()
    seed = f"{user.cpf}_{hoje.month}_{hoje.year}"
    random.seed(seed)
    
    transacoes = []
    
    # Random income transfers (Gig worker / Uber: R$ 5 to R$ 200)
    num_entradas = random.randint(20, 80)
    for _ in range(num_entradas):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': 'PIX_RECEBIDO',
            'valor': round(random.uniform(5, 200), 2),
            'descricao': 'Recebimento de Corridas (App)'
        })
        
    # Random expenses
    num_saidas = random.randint(2, 6)
    for _ in range(num_saidas):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': random.choice(['BOLETO_PAGO', 'COMPRA_CARTAO']),
            'valor': round(random.uniform(100, 3000), 2),
            'descricao': 'Despesa Corporativa'
        })
        
    random.seed()  # reset seed so we don't affect standard randomization processes
    return transacoes

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def analisar_credito(request):
    user = request.user
    
    # Instead of trusting frontend, we 'fetch' from our Open Finance provider mock
    transacoes = fetch_belvo_transactions(user)
    
    renda_total = 0.0
    despesa_total = 0.0
    
    # Motor Lendo o Extrato
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
        cor = "green"
    elif score_final >= 500:
        status = "Microcrédito Aprovado"
        cor = "orange"
    else:
        status = "Crédito Negado"
        cor = "red"

    return Response({
        "score": score_final,
        "status": status,
        "cor": cor,
        "detalhes": {
            "renda_calculada": f"R$ {renda_total:.2f}",
            "despesa_calculada": f"R$ {despesa_total:.2f}",
            "qtd_transacoes_analisadas": len(transacoes)
        },
        "transacoes": transacoes
    })