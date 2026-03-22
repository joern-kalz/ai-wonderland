"""Represents a game session."""

from dataclasses import dataclass

from src.model.chat_message import ChatMessage
from src.model.npc import Npc


@dataclass
class GameSession:
    """Represents a game session."""

    crisis: str
    quests: list[str]
    actions_since_quest_start: int
    npcs_by_name: dict[str, Npc]
    current_npc: str
    log: list[ChatMessage]
