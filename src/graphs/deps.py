import os
from collections.abc import Callable
from typing_extensions import TypedDict

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from src.graphs.router.area.methods import AREA_TOOLS


DEFAULT_MODEL = "google/gemini-2.0-flash-001"
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"


class Deps(TypedDict):
    build_llm: Callable[[float | None], ChatOpenAI]
    get_area_tools: Callable[[], list[BaseTool]]


def build_default_deps() -> Deps:
    def get_api_key() -> str:
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if api_key is None:
            raise ValueError("OPENROUTER_API_KEY is required")
        return api_key

    def build_llm(temperature: float | None = None) -> ChatOpenAI:
        kwargs = {
            "model": DEFAULT_MODEL,
            "api_key": get_api_key,
            "base_url": DEFAULT_BASE_URL,
        }
        if temperature is not None:
            kwargs["temperature"] = temperature
        return ChatOpenAI(**kwargs)

    def get_area_tools() -> list[BaseTool]:
        return AREA_TOOLS

    return {"build_llm": build_llm, "get_area_tools": get_area_tools}
