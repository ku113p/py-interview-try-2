"""Area loop tools and tool registry."""

import logging
import sqlite3

from langchain.tools import tool
from langchain_core.messages.tool import ToolCall

from src.infrastructure.db import repositories as db

from .methods import CriteriaMethods, CurrentAreaMethods, LifeAreaMethods
from .schemas import (
    CreateCriteriaArgs,
    CreateLifeAreaArgs,
    DeleteCriteriaArgs,
    DeleteLifeAreaArgs,
    GetLifeAreaArgs,
    ListCriteriaArgs,
    ListLifeAreasArgs,
    SetCurrentAreaArgs,
)
from .validators import validate_uuid_args

logger = logging.getLogger(__name__)


async def call_tool(tool_call: ToolCall, conn: sqlite3.Connection | None = None):
    tool_name = tool_call["name"]
    tool_args = dict(tool_call.get("args", {}) or {})
    tool_args.pop("conn", None)

    tool_fn = TOOL_METHODS.get(tool_name)

    if tool_fn is None:
        raise KeyError(f"Unknown tool: {tool_name}")
    logger.info(
        "Calling tool",
        extra={
            "tool_name": tool_name,
            "arg_keys": list(tool_args.keys()),
            "tool_args": tool_args,
        },
    )
    return tool_fn(**tool_args, conn=conn)


@tool(args_schema=ListLifeAreasArgs)
@validate_uuid_args("user_id")
def list_life_areas(user_id: str) -> list[db.LifeArea]:
    """List all life areas for a user."""
    return LifeAreaMethods.list(user_id)


@tool(args_schema=GetLifeAreaArgs)
@validate_uuid_args("user_id", "area_id")
def get_life_area(user_id: str, area_id: str) -> db.LifeArea:
    """Fetch a single life area by id for a user."""
    return LifeAreaMethods.get(user_id, area_id)


@tool(args_schema=CreateLifeAreaArgs)
@validate_uuid_args("user_id", "parent_id")
def create_life_area(
    user_id: str, title: str, parent_id: str | None = None
) -> db.LifeArea:
    """Create a new life area for a user."""
    return LifeAreaMethods.create(user_id, title, parent_id)


@tool(args_schema=DeleteLifeAreaArgs)
@validate_uuid_args("user_id", "area_id")
def delete_life_area(user_id: str, area_id: str) -> None:
    """Delete a life area by id for a user."""
    LifeAreaMethods.delete(user_id, area_id)


@tool(args_schema=ListCriteriaArgs)
@validate_uuid_args("user_id", "area_id")
def list_criteria(user_id: str, area_id: str) -> list[db.Criteria]:
    """List criteria belonging to a life area."""
    return CriteriaMethods.list(user_id, area_id)


@tool(args_schema=DeleteCriteriaArgs)
@validate_uuid_args("user_id", "criteria_id")
def delete_criteria(user_id: str, criteria_id: str) -> None:
    """Delete a criteria item by id for a user."""
    CriteriaMethods.delete(user_id, criteria_id)


@tool(args_schema=CreateCriteriaArgs)
@validate_uuid_args("user_id", "area_id")
def create_criteria(user_id: str, area_id: str, title: str) -> db.Criteria:
    """Create a criteria item under a life area."""
    return CriteriaMethods.create(user_id, area_id, title)


@tool(args_schema=SetCurrentAreaArgs)
@validate_uuid_args("user_id", "area_id")
def set_current_area(user_id: str, area_id: str) -> db.LifeArea:
    """Set a life area as the current area for interview. Call this after creating an area when the user wants to be interviewed about it."""
    return CurrentAreaMethods.set_current(user_id, area_id)


AREA_TOOLS = [
    create_life_area,
    delete_life_area,
    get_life_area,
    list_life_areas,
    create_criteria,
    delete_criteria,
    list_criteria,
    set_current_area,
]

TOOL_METHODS = {
    "list_life_areas": LifeAreaMethods.list,
    "get_life_area": LifeAreaMethods.get,
    "create_life_area": LifeAreaMethods.create,
    "delete_life_area": LifeAreaMethods.delete,
    "list_criteria": CriteriaMethods.list,
    "delete_criteria": CriteriaMethods.delete,
    "create_criteria": CriteriaMethods.create,
    "set_current_area": CurrentAreaMethods.set_current,
}
