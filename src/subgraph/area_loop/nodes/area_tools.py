import time
from typing import Annotated, cast

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src.message_buckets import MessageBuckets, merge_message_buckets
from src.subgraph.area_loop.tools import call_tool


class State(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    messages_to_save: Annotated[MessageBuckets, merge_message_buckets]
    success: bool | None = None


async def _build_tool_message(tool_call: dict) -> tuple[ToolMessage, bool]:
    try:
        tool_result = await call_tool(tool_call)
        content = str(tool_result)
        success = True
    except Exception as exc:
        content = f"tool_error: {type(exc).__name__}: {exc}"
        success = False

    return (
        ToolMessage(
            content=content,
            tool_call_id=tool_call["id"],
            name=tool_call["name"],
        ),
        success,
    )


async def area_tools(state: State):
    last_message = state.messages[-1]

    tools_messages = []
    messages_to_save: MessageBuckets = {}
    success = state.success if state.success is not None else True
    tool_calls = cast(list, getattr(last_message, "tool_calls", None) or [])
    for tool_call in tool_calls:
        t_msg, call_success = await _build_tool_message(tool_call)
        if not call_success:
            success = False
        tools_messages.append(t_msg)
        ts = time.time()
        if ts in messages_to_save:
            messages_to_save[ts].append(t_msg)
        else:
            messages_to_save[ts] = [t_msg]

    return {
        "messages": tools_messages,
        "messages_to_save": messages_to_save,
        "success": success,
    }
