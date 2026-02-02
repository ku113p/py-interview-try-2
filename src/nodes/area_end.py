from pydantic import BaseModel


class State(BaseModel):
    messages: list


def area_end(state: State):
    return state
