import os
import requests

# Usually credentials would be in settings, loaded from .env
BELVO_SECRET_ID = os.getenv("BELVO_SECRET_ID", "")
BELVO_SECRET_PASSWORD = os.getenv("BELVO_SECRET_PASSWORD", "")
BELVO_ENVIRONMENT = os.getenv("BELVO_ENVIRONMENT", "sandbox")

BASE_URL = f"https://{BELVO_ENVIRONMENT}.belvo.com"

def get_belvo_auth():
    return (BELVO_SECRET_ID, BELVO_SECRET_PASSWORD)

def generate_widget_token():
    """Generates an access token so the frontend widget can load safely"""
    url = f"{BASE_URL}/api/token/"
    
    # Needs to match Belvo API docs: Send secret ID and password.
    # Actually, for Widget widget token, it is usually /api/token/.
    # Standard Belvo requires HTTP Basic Auth with Secret ID and Password.
    response = requests.post(
        url,
        auth=get_belvo_auth(),
        json={
            "id": BELVO_SECRET_ID,
            "password": BELVO_SECRET_PASSWORD,
            "scopes": "read_institutions,write_links,read_transactions"
        }
    )
    if response.status_code == 200:
        return response.json().get("access")
    return None

def fetch_link_transactions(link_id):
    """Retrieve transactions associated with a given link"""
    url = f"{BASE_URL}/api/transactions/"
    
    # We query transactions for the given link_id
    response = requests.get(
        url,
        auth=get_belvo_auth(),
        params={"link": link_id}
    )
    
    if response.status_code == 200:
        return response.json().get("results", [])
    
    return []
