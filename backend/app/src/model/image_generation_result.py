"""Represents the result of generating an NPC image."""

from dataclasses import dataclass
from src.model.chat_message import ChatMessage


@dataclass
class ImageGenerationResult:
    """Represents the result of generating an NPC image."""

    image: bytes
    log: list[ChatMessage]
