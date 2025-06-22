import json
from fastapi.routing import APIRouter
from fastapi import Request, Query
from config import redis_client, SCOPES, REDIRECT_URI, google_creds
from fastapi.responses import JSONResponse
from google_auth_oauthlib.flow import Flow

router = APIRouter()

@router.get("/gmail-mcp-callback")
async def oauth_callback(request: Request, state: str = Query(...), code: str = Query(...)):
    flow = Flow.from_client_config(
        google_creds,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
        state=state
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    # Save credentials in redis against state
    redis_key = f"gmail:credentials:{state}"
    await redis_client.set(redis_key, credentials.to_json())
    credentials = await redis_client.get(redis_key)
    return JSONResponse(json.loads(credentials), status_code=200)
