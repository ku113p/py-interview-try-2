from typing import Annotated
from pydantic import BaseModel

from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

from src.routers.area_router import AREA_TOOLS


class State(BaseModel):
    loop_step: int
    messages: Annotated[list[BaseMessage], add_messages]


def area_chat(state: State, llm: ChatOpenAI):
    llm.bind_tools(AREA_TOOLS)
    return {"messages": llm.invoke(state["messages"])}
