"""Representation of a chat message in a conversation between the user and an LLM."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class ToolCall:
    """Represents a tool call in a chat conversation."""

    id: str
    name: str
    arguments: str


@dataclass
class SystemChatMessage:
    """Represents a system message in a chat conversation."""

    role: Literal["system"]
    content: str


@dataclass
class UserChatMessage:
    """Represents a user message in a chat conversation."""

    role: Literal["user"]
    content: str


@dataclass
class AssistantChatMessage:
    """Represents an assistant message in a chat conversation."""

    role: Literal["assistant"]
    content: str
    tool_calls: list[ToolCall]


@dataclass
class ToolChatMessage:
    """Represents a tool message in a chat conversation."""

    role: Literal["tool"]
    content: str
    tool_call_id: str


ChatMessage = (
    SystemChatMessage | UserChatMessage | AssistantChatMessage | ToolChatMessage
)
