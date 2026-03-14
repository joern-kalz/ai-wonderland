"""Represents an overview of the game."""

from dataclasses import dataclass


@dataclass
class GameOverview:
    """Represents an overview of the game."""

    crisis: str
    quests: list[str]
    current_npc: str
