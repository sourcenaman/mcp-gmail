import traceback, json
from mcp.server.fastmcp import FastMCP, Context
from mcp_servers.gmail.src import GmailServer
from config import redis_client
from mcp_servers.gmail.gmail import GmailAPI
from custom_exceptions import InvalidCredentialsError, SessionNotFoundError

mcp = FastMCP(name="Gmail MCP")

async def requires_session(ctx: Context):
    try:
        session_id = dict(ctx.request_context.request.headers).get('mcp-session-id')
        print(f"Session ID: {session_id}")
        if not session_id:
            raise SessionNotFoundError("Session ID is required in the request headers.")
        credentials = await redis_client.get(f"gmail:credentials:{session_id}")
        if not credentials:
            auth_url = GmailAPI.generate_oauth_url(session_id)
            raise SessionNotFoundError(f"🔗 Please authenticate with Gmail: {auth_url}")
        try:
            credentials = GmailAPI.validate_credentials(json.loads(credentials))
            await redis_client.set(f"gmail:credentials:{session_id}", credentials)
        except InvalidCredentialsError:
            auth_url = GmailAPI.generate_oauth_url(session_id)
            raise SessionNotFoundError(f"🔗 Please re-authenticate with Gmail: {auth_url}")

        return session_id
    except ValueError as e:
        return f"🔒 Auth failed: {e}"

@mcp.tool(description="Get Gmail labels")
async def get_email_labels(
    ctx: Context
):
    try:
        session_id = await requires_session(ctx)
    except SessionNotFoundError as e:
        return str(e)
    
    gmail = await GmailServer.load(redis_client, session_id)
    labels = await gmail.get_gmail_labels()
    return f"📧 Gmail Labels: {labels}"


