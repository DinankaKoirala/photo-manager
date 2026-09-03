import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build 


SCOPES = [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/photoslibrary.readonly",
]

TOKENS_DIR = "tokens"

def get_service(account_name):
    os.makedirs(TOKENS_DIR, exist_ok=True)
    token_path = os.path.join(TOKENS_DIR, f"{account_name}.pkl")
    creds = None
    if os.path.exists(token_path):
        with open(token_path, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

            with open(token_path, "wb") as f:
                pickle.dump(creds, f)

    service = build("drive", "v3", credentials=creds)
    return service, creds

def list_accounts():
    if not os.path.exists(TOKENS_DIR):
        return[]
    files = os.listdir(TOKENS_DIR)
    return [f.replace(".pkl", "") for f in files if f.endswith(".pkl")]
