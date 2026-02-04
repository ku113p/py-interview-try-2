import time
from typing import Annotated

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src.domain import user
from src.message_buckets import MessageBuckets, merge_message_buckets


class State(BaseModel):
    user: user.User
    text: str
    messages: Annotated[list[BaseMessage], add_messages]
    messages_to_save: Annotated[MessageBuckets, merge_message_buckets]


async def build_user_message(state: State):
    new_msg = HumanMessage(content=state.text)

    return {"messages": [new_msg], "messages_to_save": {time.time(): [new_msg]}}
