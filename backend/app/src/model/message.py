"""Represents a message in a chat conversation."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class ChatMessage:
    """Represents a message in a chat conversation."""

    role: Literal["system", "user", "assistant"]
    content: str
