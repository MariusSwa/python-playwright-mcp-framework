import os

MCP_ENABLED = os.getenv("MCP_ENABLED", "false").lower() == "true"


def is_mcp_enabled() -> bool:
    return MCP_ENABLED