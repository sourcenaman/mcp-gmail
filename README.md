# Mail Summary FastAPI/MCP Server

This project is a proof-of-concept (PoC) for building an MCP (Model Context Protocol) server within a FastAPI application, with authentication and Redis caching already implemented.

**Current Status:**
- MCP integrated with FastAPI
- Authentication for secured API access
- Redis used for caching credentials

**Future Scope:**
- Read Gmail emails and provide smart summaries (e.g., "Summarize all the newsletters I got last week.")
- Full Docker support for deployment

**Quick Start:**
1. Clone the repo and set up your `.env` with Gmail and Redis credentials.
2. Build and run with Docker:
   ```sh
   docker build -t mail-summary .
   docker run --env-file .env -p 8000:8000 mail-summary
   ```

See the code for more details.
