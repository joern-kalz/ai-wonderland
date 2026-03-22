"""Represents an overview of the game."""

from dataclasses import dataclass
from src.model.chat_message import ChatMessage


@dataclass
class GameOverview:
    """Represents an overview of the game."""

    crisis: str
    quests: list[str]
    current_npc: str
    log: list[ChatMessage]
