from mcp.server.fastmcp import FastMCP

mcp = FastMCP("self-healing-locators")


def build_locator_suggestion(
    old_locator: dict,
    page_snapshot: dict,
    intent: str,
    error_message: str = "",
) -> dict:
    """
    Suggests one structured replacement locator.

    This local implementation is intentionally conservative: it only returns
    high confidence when the page exposes a single strong candidate of the
    same locator family.
    """
    locator_type = old_locator.get("type")

    if locator_type == "role":
        return _suggest_role_locator(old_locator, page_snapshot, intent)

    if locator_type == "label":
        return _suggest_label_locator(old_locator, page_snapshot)

    if locator_type == "placeholder":
        return _suggest_placeholder_locator(old_locator, page_snapshot)

    if locator_type == "test_id":
        return _suggest_test_id_locator(old_locator, page_snapshot)

    return {
        "old_locator": old_locator,
        "replacement_locator": None,
        "intent": intent,
        "confidence": 0.0,
        "reason": f"No repair strategy is available for locator type {locator_type}.",
        "error_message": error_message,
    }


def _suggest_role_locator(old_locator: dict, page_snapshot: dict, intent: str) -> dict:
    role = old_locator.get("role")
    if not isinstance(role, str):
        return _no_suggestion(
            old_locator,
            intent,
            "Role locator repair requires a string role value.",
        )

    candidate_groups = {
        "button": page_snapshot.get("buttons", []),
        "link": page_snapshot.get("links", []),
        "heading": page_snapshot.get("headings", []),
    }
    candidates = [
        item for item in candidate_groups.get(role, [])
        if item.get("text") or item.get("ariaLabel")
    ]

    if len(candidates) != 1:
        return _no_suggestion(
            old_locator,
            intent,
            f"Expected exactly one visible {role} candidate, found {len(candidates)}.",
        )

    candidate = candidates[0]
    name = candidate.get("ariaLabel") or candidate.get("text")
    return {
        "old_locator": old_locator,
        "replacement_locator": {
            "type": "role",
            "role": role,
            "name": name,
            "exact": True,
        },
        "intent": intent,
        "confidence": 0.96,
        "reason": (
            f"The original {role} locator failed, and the page has exactly one "
            f"visible {role} candidate: {name}."
        ),
    }


def _suggest_label_locator(old_locator: dict, page_snapshot: dict) -> dict:
    labels = [item for item in page_snapshot.get("labels", []) if item.get("text")]
    if len(labels) != 1:
        return _no_suggestion(
            old_locator,
            "label",
            f"Expected exactly one visible label candidate, found {len(labels)}.",
        )

    value = labels[0]["text"]
    return {
        "old_locator": old_locator,
        "replacement_locator": {
            "type": "label",
            "value": value,
        },
        "intent": "label",
        "confidence": 0.96,
        "reason": f"The page has exactly one visible label candidate: {value}.",
    }


def _suggest_placeholder_locator(old_locator: dict, page_snapshot: dict) -> dict:
    inputs = [item for item in page_snapshot.get("inputs", []) if item.get("placeholder")]
    if len(inputs) != 1:
        return _no_suggestion(
            old_locator,
            "placeholder",
            f"Expected exactly one visible placeholder candidate, found {len(inputs)}.",
        )

    value = inputs[0]["placeholder"]
    return {
        "old_locator": old_locator,
        "replacement_locator": {
            "type": "placeholder",
            "value": value,
        },
        "intent": "placeholder",
        "confidence": 0.96,
        "reason": f"The page has exactly one visible placeholder candidate: {value}.",
    }


def _suggest_test_id_locator(old_locator: dict, page_snapshot: dict) -> dict:
    test_ids = [item for item in page_snapshot.get("testIds", []) if item.get("testId")]
    if len(test_ids) != 1:
        return _no_suggestion(
            old_locator,
            "test_id",
            f"Expected exactly one visible test id candidate, found {len(test_ids)}.",
        )

    value = test_ids[0]["testId"]
    return {
        "old_locator": old_locator,
        "replacement_locator": {
            "type": "test_id",
            "value": value,
        },
        "intent": "test_id",
        "confidence": 0.96,
        "reason": f"The page has exactly one visible test id candidate: {value}.",
    }


def _no_suggestion(old_locator: dict, intent: str, reason: str) -> dict:
    return {
        "old_locator": old_locator,
        "replacement_locator": None,
        "intent": intent,
        "confidence": 0.0,
        "reason": reason,
    }


@mcp.tool()
def suggest_locator(
    old_locator: dict,
    page_snapshot: dict,
    intent: str,
    error_message: str = "",
) -> dict:
    """
    Suggests a replacement locator when a Playwright locator fails.
    """
    return build_locator_suggestion(
        old_locator=old_locator,
        page_snapshot=page_snapshot,
        intent=intent,
        error_message=error_message,
    )


if __name__ == "__main__":
    mcp.run()
