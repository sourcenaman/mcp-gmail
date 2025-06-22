from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from config import SCOPES, REDIRECT_URI, google_creds
from custom_exceptions import InvalidCredentialsError

class GmailAPI:
  def __init__(self, credentials):
    self.creds = Credentials.from_authorized_user_info(credentials, SCOPES)

  def get_labels(self):
    service = build("gmail", "v1", credentials=self.creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])
    return labels

  @classmethod
  def validate_credentials(cls, credentials: dict):
    """Validates the credentials and returns a service object."""
    creds = Credentials.from_authorized_user_info(credentials, SCOPES)
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        raise InvalidCredentialsError("Invalid credentials")
    return creds.to_json()

  @classmethod
  def generate_oauth_url(cls, code: str):
    flow = Flow.from_client_config(
        google_creds,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        state=code  # Pass your code as state
    )
    return {"url": auth_url}
