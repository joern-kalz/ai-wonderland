from dataclasses import asdict
import os
from groq import Groq, omit
from dotenv import load_dotenv

from src.model.message import ChatMessage

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def invoke_llama(
    messages: list[ChatMessage] | str,
    temperature: float | None = None,
    json_response: bool | None = None,
) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=_convert_messages(messages),
        response_format={"type": "json_object"} if json_response == True else omit,
        temperature=temperature if temperature is not None else omit,
    )
    return response.choices[0].message.content or ""


def _convert_messages(messages: list[ChatMessage] | str) -> list:
    if isinstance(messages, list):
        return [asdict(message) for message in messages]
    else:
        return [{"role": "user", "content": messages}]
