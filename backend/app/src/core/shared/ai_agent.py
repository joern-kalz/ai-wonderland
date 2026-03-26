import random
import re
import string

from groq import BadRequestError

from src.model.chat_message import (
    ChatMessage,
    SystemChatMessage,
    ToolCall,
    ToolChatMessage,
    UserChatMessage,
    AssistantChatMessage,
)
from src.model.tool import Tool
from src.adapters.ai.text_to_text_model import invoke_text_to_text_model
import json


def invoke_json_agent(
    messages: list[ChatMessage],
    tools: list[Tool],
    max_iterations: int,
    json_prompt: str,
) -> list[ChatMessage]:
    """Invokes the AI agent loop."""

    new_messages = invoke_agent(messages, tools, max_iterations)
    text = new_messages[-1].content
    prompt = f"Use the following information to construct the JSON output:\n\n{text}"

    response = invoke_text_to_text_model(
        messages=[
            SystemChatMessage(role="system", content=json_prompt),
            UserChatMessage(role="user", content=prompt),
        ],
        json_response=True,
    )

    return new_messages + [response]


def invoke_agent(
    messages: list[ChatMessage],
    tools: list[Tool],
    max_iterations: int,
) -> list[ChatMessage]:
    """Invokes the tool call loop."""

    new_messages = messages.copy()
    tool_specs = [tool.spec for tool in tools]
    tool_map = {tool.spec.name: tool for tool in tools}

    for iteration in range(max_iterations):
        allow_tool_calls = iteration < max_iterations - 1

        try:
            assistant_message = invoke_text_to_text_model(
                messages=new_messages,
                tool_specs=tool_specs,
                allow_tool_calls=allow_tool_calls,
            )
        except BadRequestError as e:
            match = re.search(r"<function\s*=\s*(\w+)\s*(\{[^}]+\})", e.message)

            if not match:
                raise

            print("Model attempted to call a tool but there was an error: ", e.message)

            assistant_message = AssistantChatMessage(
                role="assistant",
                content="",
                tool_calls=[
                    ToolCall(
                        id="".join(
                            random.choices(string.ascii_lowercase + string.digits, k=9)
                        ),
                        name=match.group(1),
                        arguments=match.group(2).replace("\\'", "'"),
                    )
                ],
            )

        new_messages += [assistant_message]

        if not assistant_message.tool_calls:
            break

        tool_messages = _call_tools(tool_map, assistant_message.tool_calls or [])
        new_messages += tool_messages

    return new_messages


def _call_tools(
    tool_map: dict[str, Tool], requests: list[ToolCall]
) -> list[ChatMessage]:
    tool_messages: list[ChatMessage] = []

    for tool_call in requests:
        tool = tool_map.get(tool_call.name)
        if tool:
            try:
                arguments = json.loads(tool_call.arguments)
                result = tool.function(**arguments)
            except (json.JSONDecodeError, TypeError) as e:
                result = f"Error executing tool: {str(e)}"

            tool_message: ChatMessage = ToolChatMessage(
                role="tool",
                content=result,
                tool_call_id=tool_call.id,
            )

            tool_messages.append(tool_message)

    return tool_messages
