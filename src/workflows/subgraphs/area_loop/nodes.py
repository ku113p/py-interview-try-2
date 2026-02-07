"""Area loop graph nodes."""

import logging
import sqlite3
from typing import cast

from langchain_core.messages import SystemMessage, ToolMessage
from langchain_core.messages.tool import ToolCall

from src.infrastructure.db import transaction
from src.shared.message_buckets import MessageBuckets
from src.shared.timestamp import get_timestamp
from src.workflows.subgraphs.area_loop.state import AreaState
from src.workflows.subgraphs.area_loop.tools import AREA_TOOLS, call_tool

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# area_chat node
# -----------------------------------------------------------------------------


async def area_chat(state: AreaState, llm):
    """Process user input and generate response with tool calls."""
    logger.info("Running area chat", extra={"message_count": len(state.messages)})
    model = llm.bind_tools(AREA_TOOLS)
    system_message = SystemMessage(
        f"You are a helpful assistant for managing life areas (also called topics) and their criteria. "
        f"You have access to tools to create, view, modify, and delete life areas and their criteria. "
        f"User ID: {state.user.id}\n\n"
        f"Use the available tools for area CRUD operations when the user wants to:\n"
        f"- Create, edit, delete, or view life areas\n"
        f"- Create, edit, delete, or list criteria for a life area\n"
        f"- Switch to or discuss a specific life area\n"
        f"- Set a life area as current for interview\n\n"
        f"IMPORTANT: When working with criteria:\n"
        f"- Area IDs are UUIDs (e.g., '06985990-c0d4-7293-8000-...')\n"
        f"- If you don't know the area_id, call 'list_life_areas' first\n"
        f"- Extract the 'id' field from responses, never use the title as area_id\n\n"
        f"IMPORTANT: After creating a life area, ALWAYS ask the user:\n"
        f"'Would you like to set this area as the current area for interview?'\n"
        f"If they say yes, use 'set_current_area' tool with the area_id.\n"
        f"This ensures the interview will use this area and its criteria.\n\n"
        f"You should also help users by:\n"
        f"- Suggesting relevant criteria for their topics when asked\n"
        f"- Providing examples and recommendations\n"
        f"- Answering questions about life areas and criteria\n"
        f"- Being conversational and helpful, not just executing tools\n\n"
        f"Choose the appropriate tools based on the user's intent, "
        f"but also engage in helpful conversation when the user needs guidance or suggestions."
    )
    message = await model.ainvoke([system_message, *state.messages])
    return {"messages": [message], "messages_to_save": {get_timestamp(): [message]}}


# -----------------------------------------------------------------------------
# area_tools node
# -----------------------------------------------------------------------------


class ToolExecutionError(Exception):
    """Error during tool execution with associated ToolMessage."""

    def __init__(self, message: ToolMessage) -> None:
        super().__init__("Tool execution failed")
        self.message = message


def _validate_tool_call(call_dict: dict[str, object]) -> tuple[str, str]:
    """Validate tool call structure and return (call_id, call_name)."""
    if not isinstance(call_dict, dict):
        raise ToolExecutionError(
            ToolMessage(
                content="tool_error: ValidationError: tool_call must be a dictionary",
                tool_call_id="unknown",
                name="unknown",
            )
        )
    call_id = call_dict.get("id", "unknown")
    call_name = call_dict.get("name", "unknown")
    if not isinstance(call_id, str) or not isinstance(call_name, str):
        raise ToolExecutionError(
            ToolMessage(
                content="tool_error: ValidationError: tool_call missing required fields",
                tool_call_id=str(call_id),
                name=str(call_name),
            )
        )
    return call_id, call_name


async def _execute_tool_call(
    call: dict[str, object], conn: sqlite3.Connection
) -> ToolMessage:
    """Execute a single tool call and return the result message."""
    call_id, call_name = _validate_tool_call(call)
    try:
        result = await call_tool(cast(ToolCall, call), conn=conn)
    except Exception as exc:
        raise ToolExecutionError(
            ToolMessage(
                content=f"tool_error: {type(exc).__name__}: {exc}",
                tool_call_id=call_id,
                name=call_name,
            )
        ) from exc
    return ToolMessage(content=str(result), tool_call_id=call_id, name=call_name)


def _make_result(
    messages: list[ToolMessage], messages_to_save: MessageBuckets, success: bool
) -> dict[str, list[ToolMessage] | MessageBuckets | bool]:
    """Create a result dict for area_tools."""
    return {
        "messages": messages,
        "messages_to_save": messages_to_save,
        "success": success,
    }


async def _run_tool_calls(
    tool_calls: list[dict[str, object]],
) -> tuple[list[ToolMessage], MessageBuckets]:
    """Execute all tool calls within a transaction."""
    messages: list[ToolMessage] = []
    messages_to_save: MessageBuckets = {}
    with transaction() as conn:
        conn = cast(sqlite3.Connection, conn)
        for call in tool_calls:
            msg = await _execute_tool_call(call, conn)
            messages.append(msg)
            messages_to_save.setdefault(get_timestamp(), []).append(msg)
    return messages, messages_to_save


async def area_tools(state: AreaState):
    """Execute tool calls from the last message."""
    tool_calls = cast(
        list[dict[str, object]],
        getattr(state.messages[-1], "tool_calls", None) or [],
    )
    if not tool_calls:
        return _make_result([], {}, state.success)

    logger.info("Executing tool calls", extra={"count": len(tool_calls)})
    try:
        messages, messages_to_save = await _run_tool_calls(tool_calls)
    except ToolExecutionError as exc:
        logger.warning("Tool execution error")
        return _make_result([exc.message], {get_timestamp(): [exc.message]}, False)
    except Exception:
        logger.exception("Unexpected tool execution failure")
        fallback = ToolMessage(
            content="tool_error: ToolFailure", tool_call_id="unknown", name="unknown"
        )
        return _make_result([fallback], {get_timestamp(): [fallback]}, False)

    success = state.success if state.success is not None else True
    logger.info("Tool handling completed", extra={"success": success})
    return _make_result(messages, messages_to_save, success)


# -----------------------------------------------------------------------------
# area_end node
# -----------------------------------------------------------------------------


def area_end(state: AreaState):
    """Finalize the area loop, setting success if not already set."""
    if state.success is None:
        return {"success": True}
    return {}
