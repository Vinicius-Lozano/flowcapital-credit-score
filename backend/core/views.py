import random
from datetime import date
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

def fetch_belvo_transactions(user):
    """
    Mock integration simulation.
    Generates deterministic data based on user CPF.
    """
    hoje = date.today()
    seed = f"{user.cpf}_{hoje.month}_{hoje.year}"
    random.seed(seed)
    
    transacoes = []
    
    # Random income
    for _ in range(random.randint(15, 30)):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': 'PIX_RECEBIDO',
            'valor': round(random.uniform(50, 500), 2),
            'descricao': 'Recebimento de Cliente'
        })
        
    # Random expenses
    for _ in range(random.randint(5, 15)):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': 'COMPRA_CARTAO',
            'valor': round(random.uniform(20, 1000), 2),
            'descricao': 'Fornecedores e Serviços'
        })
        
    random.seed()
    return transacoes

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def analisar_credito(request):
    """
    Analyzes banking data using simulation.
    """
    user = request.user
    transacoes = fetch_belvo_transactions(user)
    
    renda_total = sum(float(t['valor']) for t in transacoes if t['tipo'] == 'PIX_RECEBIDO')
    despesa_total = sum(float(t['valor']) for t in transacoes if t['tipo'] != 'PIX_RECEBIDO')

    # Algorithm
    score = 300 
    if renda_total > (despesa_total * 1.5):
        score += 450
    elif renda_total > despesa_total:
        score += 250
    else:
        score -= 100
        
    score_final = max(0, min(1000, int(score)))

    if score_final >= 700:
        status, cor = "Crédito Aprovado!", "green"
    elif score_final >= 500:
        status, cor = "Microcrédito Aprovado", "orange"
    else:
        status, cor = "Crédito Negado", "red"

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