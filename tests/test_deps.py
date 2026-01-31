import pytest

from src.graphs import deps as deps_module
from src.graphs.router.area.methods import AREA_TOOLS


def test_build_default_deps_uses_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    built = deps_module.build_default_deps()
    llm = built["build_llm"](temperature=0)
    assert llm.model_name == deps_module.DEFAULT_MODEL
    assert built["get_area_tools"]() is AREA_TOOLS
