import enum
import uuid
from typing import Annotated, Literal
from typing_extensions import NotRequired, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import START, StateGraph, END
from langgraph.graph.message import add_messages

from src.domain import user
from .interview.node import build_interview_node
from .area.graph import get_subgraph as area_subgraph
from src.graphs.deps import Deps


class Target(enum.Enum):
    interview = "interview"
    areas = "areas"

    @classmethod
    def from_user_mode(cls, mode: user.InputMode):
        match mode:
            case user.InputMode.interview:
                return cls.interview
            case user.InputMode.areas:
                return cls.areas
            case _:
                raise NotImplementedError()


class State(TypedDict):
    user: user.User
    target: Target
    messages: Annotated[list[BaseMessage], add_messages]
    loop_step: int
    extract_data_dir: str
    was_covered: bool
    area_id: NotRequired[uuid.UUID]


def route_message(state: State) -> Literal["area", "interview"]:
    target = state["target"]
    if target == Target.interview:
        return "interview"
    if target == Target.areas:
        return "area"

    raise ValueError(f"Unknown target: {target}")


def get_subgraph(deps: Deps):
    builder = StateGraph(State)

    builder.add_node("interview", build_interview_node(deps))
    builder.add_node("area", area_subgraph(deps))

    builder.add_conditional_edges(START, route_message, ["interview", "area"])
    builder.add_edge("interview", END)
    builder.add_edge("area", END)

    graph = builder.compile()

    return graph
