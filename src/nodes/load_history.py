from typing import Annotated

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel

from src import db
from src.domain import user


class State(BaseModel):
    user: user.User
    messages: Annotated[list[BaseMessage], add_messages]


async def load_history(state: State):
    msgs = get_formatted_history(state.user)
    return {"messages": msgs}


def get_formatted_history(user_obj: user.User, limit: int = 10) -> list[BaseMessage]:
    msgs = sorted(
        db.HistoryManager.list_by_user(user_obj.id), key=lambda x: -x.created_ts
    )
    domain_msgs = [msg.data for msg in msgs[:limit]]

    formatted_messages = []
    for msg in domain_msgs:
        if msg["role"] == "user":
            formatted_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "ai":
            formatted_messages.append(AIMessage(content=msg["content"]))
        else:
            raise NotImplementedError()

    return formatted_messages
