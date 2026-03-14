"""Represents a game session."""

from dataclasses import dataclass

from src.model.npc import Npc


@dataclass
class GameSession:
    """Represents a game session."""

    crisis: str
    quests: list[str]
    actions_since_quest_start: int
    npcs_by_name: map[str, Npc]
    current_npc: str
