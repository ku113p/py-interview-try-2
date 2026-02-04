import time
from typing import Annotated

from langchain_core.messages import AIMessage, BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src.message_buckets import MessageBuckets, merge_message_buckets


class State(BaseModel):
    messages: Annotated[list[BaseMessage], add_messages]
    messages_to_save: Annotated[MessageBuckets, merge_message_buckets]
    success: bool | None = None


async def area_threshold(state: State):
    content = "Can you say this differently? (answer generation error)"
    ai_msg = AIMessage(content=content)
    return {
        "messages": [ai_msg],
        "messages_to_save": {time.time(): [ai_msg]},
        "success": False,
    }
