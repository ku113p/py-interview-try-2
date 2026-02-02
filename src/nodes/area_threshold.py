from pydantic import BaseModel

from langchain_core.messages import AIMessage


class State(BaseModel):
    messages: list


async def area_threshold(*args, **kwargs):
    content = "Can you say this differently? (answer generation error)"
    ai_msg = AIMessage(content=content)
    return {"messages": [ai_msg]}
