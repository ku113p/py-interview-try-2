import pytest
from typing import cast

from langchain_core.messages import AIMessage

from src.graphs.router.area.graph import get_subgraph
from src.graphs.deps import Deps


def test_area_graph_requires_loop_step():
    graph = get_subgraph(build_stub_deps())
    state = {"messages": [AIMessage(content="hi", tool_calls=[])]}
    with pytest.raises(KeyError):
        graph.invoke(state)


def test_area_graph_preserves_loop_step():
    graph = get_subgraph(build_stub_deps())
    state = {"loop_step": 2, "messages": [AIMessage(content="hi", tool_calls=[])]}
    result = graph.invoke(state)
    assert result["loop_step"] == 2


def build_stub_deps() -> Deps:
    class StubLLM:
        def bind_tools(self, tools):
            class Runner:
                def invoke(self, _):
                    return [AIMessage(content="ok", tool_calls=[])]

            return Runner()

    def build_llm(temperature: float | None = None):  # noqa: ARG001
        return StubLLM()

    deps = {"build_llm": build_llm, "get_area_tools": lambda: []}
    return cast(Deps, deps)
