import json
from typing import Any
from mcp_servers.gmail.gmail import GmailAPI
from redis import Redis

class GmailServer:
    def __init__(self, session_id: str, credentials: dict[str, Any] = {}):
        self.session_id = session_id
        self.gmail_api = GmailAPI(credentials)

    @classmethod
    async def load(cls, redis: Redis, session_id: str) -> "GmailServer":
        credentials = await redis.get(f"gmail:credentials:{session_id}")
        return cls(session_id, json.loads(credentials))

    async def get_gmail_labels(self):
        labels = self.gmail_api.get_labels()
        return labels