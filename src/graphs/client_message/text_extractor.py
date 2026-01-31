import base64
import tempfile
from typing_extensions import NotRequired, TypedDict
from langchain_core.messages import HumanMessage

from src.domain import message as domain_message
from src.graphs.deps import Deps


class State(TypedDict):
    message: domain_message.ClientMessage
    audio_file: NotRequired[tempfile._TemporaryFileWrapper]
    text: NotRequired[str]


def build_text_extractor(deps: Deps):
    async def extract_text(state: State):
        c_msg = state["message"]
        if isinstance(c_msg.data, str):
            return {"text": c_msg.data}

        audio_file = state.get("audio_file")
        if audio_file is None:
            raise ValueError("Missing audio file for transcription")

        text = await extract_text_from_audio(audio_file, deps)
        return {"text": text}

    return extract_text


async def extract_text_from_audio(
    audio_file: tempfile._TemporaryFileWrapper, deps: Deps
) -> str:
    b64_audio = encode_audio(audio_file)
    llm = deps["build_llm"](temperature=0)
    message = build_prompt(b64_audio)
    response = await llm.ainvoke([message])
    return parse_transcription(response.content)


def encode_audio(audio_file: tempfile._TemporaryFileWrapper) -> str:
    audio_file.seek(0)
    audio_data = audio_file.read()
    return base64.b64encode(audio_data).decode("utf-8")


def build_prompt(b64_audio: str):
    return HumanMessage(
        content=[
            {"type": "text", "text": "Transcribe this audio verbatim."},
            {
                "type": "input_audio",
                "input_audio": {"data": b64_audio, "format": "mp3"},
            },
        ]
    )


def parse_transcription(content: object) -> str:
    if not isinstance(content, str):
        raise ValueError("Transcription failed")
    return content
