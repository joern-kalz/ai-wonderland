"""Models of the talk use case."""

from dataclasses import dataclass
from src.model.chat_message import ChatMessage


@dataclass
class EvaluationResult:
    """Represents the result of evaluating the player success."""

    success: bool
    log: list[ChatMessage]


@dataclass
class NpcResponse:
    """Represents the response from the NPC."""

    message: ChatMessage
    log: list[ChatMessage]
