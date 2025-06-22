import contextlib
from fastapi import FastAPI
from config import redis_client
from api.gmail import router as gmail_router
from mcp_servers.gmail.tools import mcp as gmail_mcp

@contextlib.asynccontextmanager
async def lifespan(app):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(gmail_mcp.session_manager.run())
        await stack.enter_async_context(redis_client)
        try:
            yield
        finally:
            await redis_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(gmail_router, prefix="/api", tags=["Gmail"])

app.mount("/tools", gmail_mcp.streamable_http_app())

