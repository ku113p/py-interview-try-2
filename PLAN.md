# Refactor and Fix Plan

Decisions
- Tests: pytest.
- CLI: text-only input loop.
- DI: factory functions to build dependencies and inject into graph builders.

Plan
1. Define a root State TypedDict that covers all graph needs.
2. Add dependency factories and pass deps into graph builders.
3. Implement tool call dispatcher in area methods.
4. Replace incomplete src/graph.py with root graph composition.
5. Normalize state keys and types across subgraphs.
6. Align async/sync nodes under a single async graph.
7. Implement minimal CLI loop in main.py.
8. Add pytest tests for nodes, subgraphs, and end-to-end.
9. Run tests and validate CLI.
