import random
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from .pluggy_service import generate_connect_token, fetch_transactions

def fetch_mock_transactions(user):
    """
    Simulação de integração para testes (Fallback).
    Gera dados determinísticos baseados no CPF do usuário.
    """
    hoje = date.today()
    seed = f"{user.cpf}_{hoje.month}_{hoje.year}"
    random.seed(seed)
    
    transacoes = []
    
    # Ganhos aleatórios (PIX Recebido)
    for _ in range(random.randint(15, 30)):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': 'PIX_RECEBIDO',
            'valor': round(random.uniform(50, 2000), 2),
            'descricao': 'Recebimento de Cliente'
        })
        
    # Gastos aleatórios (Cartão/Boletos)
    for _ in range(random.randint(10, 20)):
        transacoes.append({
            'data': hoje.isoformat(),
            'tipo': 'COMPRA_CARTAO',
            'valor': round(random.uniform(10, 1500), 2),
            'descricao': 'Fornecedores e Serviços'
        })
        
    random.seed()
    return transacoes

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
    Analisa dados da Pluggy ou Simulation
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
        # Mapeia formato Pluggy para o nosso formato interno
        for t in transacoes_pluggy:
            transacoes.append({
                'data': t.get('date'),
                'tipo': 'PIX_RECEBIDO' if float(t.get('amount', 0)) > 0 else 'COMPRA_CARTAO',
                'valor': abs(float(t.get('amount', 0))),
                'descricao': t.get('description')
            })
        origem = "Pluggy"
    else:
        # Failsafe automático
        transacoes = fetch_mock_transactions(user)
        
    renda_total = 0.0
    despesa_total = 0.0

    # Motor de Análise
    for t in transacoes:
        valor = float(t.get('valor', 0))
        if t.get('tipo') == 'PIX_RECEBIDO':
            renda_total += valor
        else:
            despesa_total += valor

    # Algoritmo de Score
    score = 300 
    if renda_total > (despesa_total * 1.5):
        score += 450
    elif renda_total > despesa_total:
        score += 250
    else:
        score -= 100
        
    score_final = max(0, min(1000, int(score)))

    # Decisão de Crédito
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
        "origem": origem,
        "detalhes": {
            "renda_calculada": f"R$ {renda_total:.2f}",
            "despesa_calculada": f"R$ {despesa_total:.2f}",
            "qtd_transacoes_analisadas": len(transacoes)
        },
        "transacoes": transacoes
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
        # Lógica para quando uma nova conexão é criada
        pass
    elif event_type == 'item/updated':
        # Lógica para quando dados são atualizados (ex: novas transações)
        pass
    elif event_type == 'item/error':
        # Lógica para tratar erros na conexão
        error_detail = event.get('error')
        print(f"Erro no item {item_id}: {error_detail}")

    # IMPORTANTE: Retornar 2XX em menos de 5 segundos
    return Response({"received": True}, status=200)