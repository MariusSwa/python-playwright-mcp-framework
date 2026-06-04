from mcp.server.fastmcp import FastMCP

mcp = FastMCP("self-healing-locators")


@mcp.tool()
def suggest_locator(old_locator: str, page_snapshot: str, intent: str) -> dict:
    """
    Suggests a replacement locator when a Playwright locator fails.
    This is a placeholder for now. Later this can call an LLM.
    """

    suggestions = []

    if "Login" in page_snapshot:
        suggestions.append("page.get_by_role('button', name='Login')")

    if "Email" in page_snapshot:
        suggestions.append("page.get_by_label('Email')")

    return {
        "old_locator": old_locator,
        "intent": intent,
        "suggestions": suggestions,
        "confidence": 0.6
    }


if __name__ == "__main__":
    mcp.run()