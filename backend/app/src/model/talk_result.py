"""Represents the result of talking to an NPC."""

from dataclasses import dataclass


@dataclass
class TalkResult:
    """Represents the result of talking to an NPC."""

    message: str
    game_end: bool
