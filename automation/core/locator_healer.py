import ast
import importlib.util
import inspect
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from playwright.sync_api import Locator, Page

from core import config

if TYPE_CHECKING:
    from core.base_page import LocatorConfig


def build_locator_suggestion(
    old_locator: dict[str, Any],
    page_snapshot: dict[str, Any],
    intent: str,
    error_message: str = "",
) -> dict[str, Any]:
    server_path = Path(__file__).resolve().parents[1] / "mcp" / "servers" / "self_healing_server.py"
    spec = importlib.util.spec_from_file_location(
        "local_self_healing_server",
        server_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load MCP server from {server_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    response = module.build_locator_suggestion(
        old_locator=old_locator,
        page_snapshot=page_snapshot,
        intent=intent,
        error_message=error_message,
    )
    return cast(dict[str, Any], response)


@dataclass(frozen=True)
class LocatorRepairConfig:
    mode: str
    min_confidence: float
    max_repairs_per_test: int
    max_attempts_per_locator: int
    max_mcp_calls_per_test: int
    history_file: Path
    is_ci: bool

    @classmethod
    def from_environment(cls) -> "LocatorRepairConfig":
        return cls(
            mode=config.LOCATOR_REPAIR_MODE,
            min_confidence=config.LOCATOR_REPAIR_MIN_CONFIDENCE,
            max_repairs_per_test=config.LOCATOR_REPAIR_MAX_REPAIRS_PER_TEST,
            max_attempts_per_locator=config.LOCATOR_REPAIR_MAX_ATTEMPTS_PER_LOCATOR,
            max_mcp_calls_per_test=config.LOCATOR_REPAIR_MAX_MCP_CALLS_PER_TEST,
            history_file=config.LOCATOR_REPAIR_HISTORY_FILE,
            is_ci=config.CI,
        )

    @property
    def enabled(self) -> bool:
        return self.mode in {"dry_run", "repair"} and not self.is_ci

    @property
    def should_patch_code(self) -> bool:
        return self.mode == "repair" and not self.is_ci


@dataclass
class LocatorRepairSuggestion:
    replacement_locator: dict[str, Any]
    confidence: float
    reason: str


@dataclass
class LocatorRepairEvent:
    timestamp: str
    test_id: str
    page_object: str
    locator_name: str | None
    action: str
    mode: str
    old_locator: dict[str, Any]
    new_locator: dict[str, Any] | None
    confidence: float | None
    status: str
    reason: str


class LocatorRepairSession:
    def __init__(self, test_id: str, repair_config: LocatorRepairConfig):
        self.test_id = test_id
        self.config = repair_config
        self.repairs_used = 0
        self.mcp_calls_used = 0
        self.locator_attempts: dict[str, int] = {}

    def can_call_mcp(self) -> bool:
        return self.mcp_calls_used < self.config.max_mcp_calls_per_test

    def can_repair(self, locator_key: str) -> bool:
        locator_attempts = self.locator_attempts.get(locator_key, 0)
        return (
            self.repairs_used < self.config.max_repairs_per_test
            and locator_attempts < self.config.max_attempts_per_locator
        )

    def record_mcp_call(self) -> None:
        self.mcp_calls_used += 1

    def record_repair(self, locator_key: str) -> None:
        self.repairs_used += 1
        self.locator_attempts[locator_key] = self.locator_attempts.get(locator_key, 0) + 1


class LocatorRepairLimiter:
    _sessions: dict[str, LocatorRepairSession] = {}

    @classmethod
    def get_session(cls, repair_config: LocatorRepairConfig) -> LocatorRepairSession:
        test_id = os.getenv("PYTEST_CURRENT_TEST", "manual-run").split(" ")[0]
        session = cls._sessions.get(test_id)
        if session is None:
            session = LocatorRepairSession(test_id, repair_config)
            cls._sessions[test_id] = session
        return session


class LocatorCodeUpdater:
    def update_locator(
        self,
        page_object_type: type,
        locator_name: str,
        replacement_locator: dict[str, Any],
    ) -> None:
        source_file = inspect.getsourcefile(page_object_type)
        if source_file is None:
            raise RuntimeError(f"Could not find source file for {page_object_type.__name__}")

        path = Path(source_file)
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        assignment = self._find_locator_assignment(
            tree,
            page_object_type.__name__,
            locator_name,
        )
        if assignment.end_lineno is None:
            raise RuntimeError(f"Could not determine end line for {locator_name}")

        lines = source.splitlines()
        indent = " " * assignment.col_offset
        replacement = self._format_assignment(indent, locator_name, replacement_locator)
        updated_lines = [
            *lines[: assignment.lineno - 1],
            *replacement.splitlines(),
            *lines[assignment.end_lineno :],
        ]
        path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")

    def _find_locator_assignment(
        self,
        tree: ast.Module,
        class_name: str,
        locator_name: str,
    ) -> ast.Assign:
        for node in tree.body:
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                for child in node.body:
                    if not isinstance(child, ast.Assign):
                        continue
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == locator_name:
                            return child
        raise RuntimeError(f"Could not find locator {class_name}.{locator_name}")

    def _format_assignment(
        self,
        indent: str,
        locator_name: str,
        locator: dict[str, Any],
    ) -> str:
        nested_indent = f"{indent}    "
        lines = [f"{indent}{locator_name} = {{"]
        for key, value in locator.items():
            lines.append(
                f"{nested_indent}{self._format_python_value(key)}: "
                f"{self._format_python_value(value)},"
            )
        lines.append(f"{indent}}}")
        return "\n".join(lines)

    def _format_python_value(self, value: Any) -> str:
        if isinstance(value, str):
            escaped = value.replace("\\", "\\\\").replace('"', '\\"')
            return f'"{escaped}"'
        return repr(value)


class LocatorHealer:
    def __init__(self, page_object: Any):
        self.page_object = page_object
        self.page: Page = page_object.page
        self.config = LocatorRepairConfig.from_environment()
        self.history = LocatorRepairHistory(self.config.history_file)
        self.code_updater = LocatorCodeUpdater()

    def repair_locator(
        self,
        locator: "LocatorConfig",
        action: str,
        error: Exception,
    ) -> "LocatorConfig | None":
        page_object_name = type(self.page_object).__name__
        locator_name = self._find_locator_name(locator)
        locator_key = (
            f"{page_object_name}.{locator_name}" if locator_name else f"{page_object_name}.dynamic"
        )

        if not self.config.enabled:
            return None

        session = LocatorRepairLimiter.get_session(self.config)
        if not session.can_call_mcp():
            self._record_event(
                locator,
                None,
                None,
                locator_name,
                action,
                "blocked",
                "MCP call limit reached for this test.",
            )
            return None

        if not session.can_repair(locator_key):
            self._record_event(
                locator,
                None,
                None,
                locator_name,
                action,
                "blocked",
                "Locator repair limit reached for this test or locator.",
            )
            return None

        session.record_mcp_call()
        suggestion = self._request_mcp_suggestion(locator, action, error)
        if suggestion is None:
            return None

        if suggestion.confidence < self.config.min_confidence:
            self._record_event(
                locator,
                suggestion.replacement_locator,
                suggestion.confidence,
                locator_name,
                action,
                "rejected",
                "Suggestion confidence was below the configured threshold.",
            )
            return None

        if not self._replacement_is_valid(suggestion.replacement_locator, action):
            self._record_event(
                locator,
                suggestion.replacement_locator,
                suggestion.confidence,
                locator_name,
                action,
                "rejected",
                "Replacement locator did not resolve to one valid element.",
            )
            return None

        if locator_name is None:
            self._record_event(
                locator,
                suggestion.replacement_locator,
                suggestion.confidence,
                locator_name,
                action,
                "rejected",
                "Dynamic locators are not source-patched automatically.",
            )
            return None

        if self.config.should_patch_code:
            self.code_updater.update_locator(
                type(self.page_object),
                locator_name,
                suggestion.replacement_locator,
            )
            status = "patched"
        else:
            status = "dry_run"

        session.record_repair(locator_key)
        self._record_event(
            locator,
            suggestion.replacement_locator,
            suggestion.confidence,
            locator_name,
            action,
            status,
            suggestion.reason,
        )

        if not self.config.should_patch_code:
            return None
        return suggestion.replacement_locator

    def _request_mcp_suggestion(
        self,
        locator: "LocatorConfig",
        action: str,
        error: Exception,
    ) -> LocatorRepairSuggestion | None:
        response = build_locator_suggestion(
            old_locator=dict(locator),
            page_snapshot=self._get_page_snapshot(),
            intent=action,
            error_message=str(error),
        )
        replacement = response.get("replacement_locator")
        confidence = response.get("confidence")
        reason = response.get("reason")

        if not isinstance(replacement, dict):
            return None
        if not isinstance(confidence, int | float):
            return None
        if not isinstance(reason, str):
            return None

        return LocatorRepairSuggestion(
            replacement_locator=replacement,
            confidence=float(confidence),
            reason=reason,
        )

    def _get_page_snapshot(self) -> dict[str, Any]:
        snapshot = self.page.evaluate(
            """() => {
                const text = (element) => (element.innerText || element.textContent || "").trim();
                const visible = (element) => {
                    const style = window.getComputedStyle(element);
                    const rect = element.getBoundingClientRect();
                    return style.visibility !== "hidden"
                        && style.display !== "none"
                        && rect.width > 0
                        && rect.height > 0;
                };
                const bySelector = (selector) => Array.from(document.querySelectorAll(selector))
                    .filter(visible)
                    .map((element) => ({
                        text: text(element),
                        ariaLabel: element.getAttribute("aria-label") || "",
                        placeholder: element.getAttribute("placeholder") || "",
                        testId: element.getAttribute("data-testid") || "",
                    }));

                return {
                    url: window.location.href,
                    title: document.title,
                    bodyText: text(document.body).slice(0, 4000),
                    buttons: bySelector("button, input[type=button], input[type=submit]"),
                    links: bySelector("a"),
                    headings: bySelector("h1, h2, h3, h4, h5, h6"),
                    labels: bySelector("label"),
                    inputs: bySelector("input, textarea, select"),
                    testIds: Array.from(document.querySelectorAll("[data-testid]"))
                        .filter(visible)
                        .map((element) => ({
                            testId: element.getAttribute("data-testid") || "",
                            text: text(element),
                        })),
                };
            }"""
        )
        return cast(dict[str, Any], snapshot)

    def _replacement_is_valid(self, locator: dict[str, Any], action: str) -> bool:
        resolved = self._resolve_locator(locator)
        if resolved.count() != 1:
            return False
        if not resolved.is_visible():
            return False
        if action in {"click", "fill", "check", "select_option"} and not resolved.is_enabled():
            return False
        return True

    def _resolve_locator(self, locator: dict[str, Any]) -> Locator:
        parent = locator.get("parent")
        if parent:
            return self._resolve_from(self._resolve_locator(parent), locator)
        return self._resolve_from(self.page, locator)

    def _resolve_from(self, target: Page | Locator, locator: dict[str, Any]) -> Locator:
        locator_type = locator.get("type")
        if locator_type == "role":
            return target.get_by_role(
                locator["role"],
                name=locator["name"],
                exact=locator.get("exact", False),
            )
        if locator_type == "label":
            return target.get_by_label(locator["value"])
        if locator_type == "placeholder":
            return target.get_by_placeholder(locator["value"])
        if locator_type == "text":
            return target.get_by_text(locator["value"])
        if locator_type == "test_id":
            return target.get_by_test_id(locator["value"])
        if locator_type == "css":
            return target.locator(locator["value"])
        raise ValueError(f"Unknown locator type: {locator_type}")

    def _find_locator_name(self, locator: "LocatorConfig") -> str | None:
        for name, value in vars(type(self.page_object)).items():
            if name.isupper() and isinstance(value, dict) and value == locator:
                return cast(str, name)
        return None

    def _record_event(
        self,
        old_locator: dict[str, Any],
        new_locator: dict[str, Any] | None,
        confidence: float | None,
        locator_name: str | None,
        action: str,
        status: str,
        reason: str,
    ) -> None:
        test_id = os.getenv("PYTEST_CURRENT_TEST", "manual-run").split(" ")[0]
        event = LocatorRepairEvent(
            timestamp=datetime.now(UTC).isoformat(),
            test_id=test_id,
            page_object=type(self.page_object).__name__,
            locator_name=locator_name,
            action=action,
            mode=self.config.mode,
            old_locator=dict(old_locator),
            new_locator=new_locator,
            confidence=confidence,
            status=status,
            reason=reason,
        )
        self.history.append(event)


class LocatorRepairHistory:
    def __init__(self, path: Path):
        self.path = path

    def append(self, event: LocatorRepairEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        events = self._read_events()
        events.append(asdict(event))
        self.path.write_text(
            json.dumps(events, indent=2),
            encoding="utf-8",
        )

    def _read_events(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            value = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        return []
