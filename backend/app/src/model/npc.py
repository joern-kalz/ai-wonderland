"""Represents a non-player character"""

from dataclasses import dataclass

from src.model.message import ChatMessage


@dataclass
class Npc:
    """Represents a non-player character"""

    image: bytes
    chat_history: list[ChatMessage]
