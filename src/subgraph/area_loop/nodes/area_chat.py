from typing import Annotated

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src.message_buckets import MessageBuckets, merge_message_buckets
from src.subgraph.area_loop.tools import AREA_TOOLS
from src.timestamp import get_timestamp


class State(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    messages_to_save: Annotated[MessageBuckets, merge_message_buckets]
    success: bool | None = None


async def area_chat(state: State, llm):
    model = llm.bind_tools(AREA_TOOLS)
    message = await model.ainvoke(state.messages)
    return {"messages": [message], "messages_to_save": {get_timestamp(): [message]}}
