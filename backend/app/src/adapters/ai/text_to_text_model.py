import os
from groq import APIStatusError, Groq, omit

from src.model.chat_message import AssistantChatMessage, ChatMessage, ToolCall
from src.model.tool import ToolSpec
from groq import BadRequestError
import re
import random
import string

_client: Groq | None = None


def initialize_text_to_text_model() -> None:
    """Initialize the text-to-text client."""
    global _client
    _client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def invoke_text_to_text_model(
    messages: list[ChatMessage],
    tool_specs: list[ToolSpec] | None = None,
    temperature: float | None = None,
    allow_tool_calls: bool = True,
    json_response: bool = False,
) -> AssistantChatMessage:
    if _client is None:
        raise RuntimeError("Call initialize_text_to_text_model() before use.")

    try:
        response = _client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=_map_messages_from_model(messages),
            tools=(
                _map_tool_specs_from_model(tool_specs)
                if tool_specs is not None
                else omit
            ),
            temperature=temperature if temperature is not None else omit,
            tool_choice="none" if allow_tool_calls == False else omit,
            response_format={"type": "json_object"} if json_response == True else omit,
        )

        message = response.choices[0].message
        content = message.content or ""
        tool_calls = (
            _map_tool_calls_to_model(message.tool_calls) if message.tool_calls else []
        )
    except BadRequestError as e:
        match = re.search(r"<function\s*=\s*(\w+)\s*(\{[^}]+\})", e.message)

        if not match:
            raise

        print("Model attempted to call a tool but there was an error: ", e.message)
        content = ""
        tool_calls = [_create_tool_call(match.group(1), match.group(2))]
    except APIStatusError as e:
        print(f"Status code: {e.status_code}")
        print(f"Response: {e.response.json()}")
        raise

    return AssistantChatMessage(
        role="assistant", content=content, tool_calls=tool_calls
    )


def _create_tool_call(name: str, arguments: str) -> ToolCall:
    return ToolCall(
        id="".join(random.choices(string.ascii_lowercase + string.digits, k=9)),
        name=name,
        arguments=arguments.replace("\\'", "'"),
    )


def _map_messages_from_model(messages: list[ChatMessage]) -> list:
    mapped_messages = []
    for message in messages:
        if message.role == "assistant":
            mapped_messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                    "tool_calls": [
                        _map_tool_call_from_model(call) for call in message.tool_calls
                    ],
                }
            )
        elif message.role == "tool":
            mapped_messages.append(
                {
                    "role": message.role,
                    "content": message.content,
                    "tool_call_id": message.tool_call_id,
                }
            )
        else:
            mapped_messages.append({"role": message.role, "content": message.content})
    return mapped_messages


def _map_tool_call_from_model(tool_call: ToolCall) -> dict:
    return {
        "id": tool_call.id,
        "function": {
            "name": tool_call.name,
            "arguments": tool_call.arguments,
        },
        "type": "function",
    }


def _map_tool_specs_from_model(tool_specs: list[ToolSpec]) -> list:
    return [_map_tool_spec_from_model(spec) for spec in tool_specs]


def _map_tool_spec_from_model(tool: ToolSpec) -> dict:
    properties = {}
    for arg in tool.arguments:
        properties[arg.name] = {
            "type": "string",
            "description": arg.description,
        }

    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": [arg.name for arg in tool.arguments],
            },
        },
    }


def _map_tool_calls_to_model(tool_calls) -> list[ToolCall]:
    """Parse tool calls from the API response."""

    parsed_calls = []
    for call in tool_calls:
        parsed_calls.append(
            ToolCall(
                id=call.id,
                name=call.function.name,
                arguments=call.function.arguments,
            )
        )

    return parsed_calls
