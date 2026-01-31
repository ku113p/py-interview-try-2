import tempfile
import uuid
from typing import Annotated, Literal
from typing_extensions import NotRequired, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from src.domain import message, user
from src.graphs.router.graph import Target
from .audio_extractor import build_audio_extractor
from .target_extractor import build_target_extractor
from .text_extractor import build_text_extractor
from src.graphs.deps import Deps


class State(TypedDict):
    user: user.User
    message: message.ClientMessage
    text: NotRequired[str]
    target: NotRequired[Target]
    messages: Annotated[list[BaseMessage], add_messages]
    loop_step: NotRequired[int]
    extract_data_dir: NotRequired[str]
    was_covered: NotRequired[bool]
    area_id: NotRequired[uuid.UUID]
    media_file: NotRequired[tempfile._TemporaryFileWrapper]
    audio_file: NotRequired[tempfile._TemporaryFileWrapper]


def route_message(state: State) -> Literal["extract_audio", "extract_text"]:
    c_msg = state["message"]
    if isinstance(c_msg.data, str):
        return "extract_text"
    return "extract_audio"


def get_subgraph(deps: Deps):
    builder = StateGraph(State)

    builder.add_node("extract_audio", build_audio_extractor())
    builder.add_node("extract_text", build_text_extractor(deps))
    builder.add_node("extract_target", build_target_extractor(deps))

    builder.add_conditional_edges(
        START, route_message, ["extract_audio", "extract_text"]
    )
    builder.add_edge("extract_audio", "extract_text")
    builder.add_edge("extract_text", "extract_target")
    builder.add_edge("extract_target", END)

    graph = builder.compile()

    return graph
