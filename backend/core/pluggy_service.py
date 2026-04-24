import os
import logging
import requests

logger = logging.getLogger(__name__)

PLUGGY_API_URL = "https://api.pluggy.ai"


def get_pluggy_api_key():
    """Autentica na Pluggy e retorna o API Key temporário"""
    client_id = os.getenv("PLUGGY_CLIENT_ID")
    client_secret = os.getenv("PLUGGY_CLIENT_SECRET")

    if not client_id or not client_secret:
        logger.error(
            "PLUGGY_CLIENT_ID ou PLUGGY_CLIENT_SECRET não configurados. "
            "CLIENT_ID presente: %s, CLIENT_SECRET presente: %s",
            bool(client_id), bool(client_secret)
        )
        return None

    try:
        response = requests.post(
            f"{PLUGGY_API_URL}/auth",
            json={
                "clientId": client_id,
                "clientSecret": client_secret
            },
            timeout=15
        )

        if response.status_code == 200:
            api_key = response.json().get("apiKey")
            if api_key:
                logger.info("Pluggy Auth OK — apiKey obtida com sucesso")
                return api_key
            logger.error("Pluggy Auth: resposta 200 mas sem apiKey no body")
            return None

        logger.error(
            "ERRO DE AUTENTICAÇÃO PLUGGY! Status: %s | Body: %s",
            response.status_code, response.text[:500]
        )
        return None

    except requests.exceptions.ConnectionError as e:
        logger.error("Pluggy Auth — erro de conexão (DNS/rede): %s", str(e))
        return None
    except requests.exceptions.Timeout:
        logger.error("Pluggy Auth — timeout após 15s")
        return None
    except Exception as e:
        logger.error("Pluggy Auth — erro inesperado: %s", str(e))
        return None


def generate_connect_token(client_user_id=None):
    """Gera o token de acesso para o Widget Pluggy Connect"""
    api_key = get_pluggy_api_key()
    if not api_key:
        return None

    try:
        payload = {}
        if client_user_id:
            payload["clientUserId"] = client_user_id

        response = requests.post(
            f"{PLUGGY_API_URL}/connect_token",
            headers={"X-API-KEY": api_key},
            json=payload,
            timeout=15
        )

        if response.status_code in [200, 201]:
            token = response.json().get("accessToken")
            if token:
                logger.info("Pluggy Connect Token gerado com sucesso")
                return token
            logger.error("Connect Token: resposta OK mas sem accessToken")
            return None

        logger.error(
            "Erro Connect Token Pluggy (%s): %s",
            response.status_code, response.text[:500]
        )
        return None

    except requests.exceptions.ConnectionError as e:
        logger.error("Connect Token — erro de conexão: %s", str(e))
        return None
    except requests.exceptions.Timeout:
        logger.error("Connect Token — timeout após 15s")
        return None
    except Exception as e:
        logger.error("Erro ao gerar Connect Token Pluggy: %s", str(e))
        return None


def fetch_transactions(item_id):
    """Busca transações de uma conta conectada via API REST"""
    api_key = get_pluggy_api_key()
    if not api_key:
        return []

    try:
        response = requests.get(
            f"{PLUGGY_API_URL}/transactions",
            headers={"X-API-KEY": api_key},
            params={"itemId": item_id},
            timeout=15
        )
        if response.status_code == 200:
            return response.json().get("results", [])

        logger.error(
            "Erro ao buscar transações (%s): %s",
            response.status_code, response.text[:500]
        )
        return []

    except requests.exceptions.ConnectionError as e:
        logger.error("Transações — erro de conexão: %s", str(e))
        return []
    except requests.exceptions.Timeout:
        logger.error("Transações — timeout após 15s")
        return []
    except Exception as e:
        logger.error("Erro ao buscar transações Pluggy: %s", str(e))
        return []
