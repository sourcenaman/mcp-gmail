import os
import redis.asyncio
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
SCOPES = os.environ.get("SCOPES", "https://www.googleapis.com/auth/gmail.readonly").split(",")
REDIRECT_URI = os.environ.get("AUTH_REDIRECT_URI", "http://localhost:8000/api/gmail-mcp-callback")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID")
GOOGLE_AUTH_URI = os.environ.get("GOOGLE_AUTH_URI")
GOOGLE_TOKEN_URI = os.environ.get("GOOGLE_TOKEN_URI")
GOOGLE_AUTH_PROVIDER_X509_CERT_URL = os.environ.get("GOOGLE_AUTH_PROVIDER_X509_CERT_URL")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URIS = os.environ.get("GOOGLE_REDIRECT_URIS", "").split(",")


redis_client = redis.asyncio.from_url(
    url=REDIS_URL,
    decode_responses=True
)

google_creds = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "project_id": GOOGLE_PROJECT_ID,
        "auth_uri": GOOGLE_AUTH_URI,
        "token_uri": GOOGLE_TOKEN_URI,
        "auth_provider_x509_cert_url": GOOGLE_AUTH_PROVIDER_X509_CERT_URL,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uris": GOOGLE_REDIRECT_URIS
    }
}
