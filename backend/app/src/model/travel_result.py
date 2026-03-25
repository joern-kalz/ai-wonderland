"""Represents the result of talking to an NPC."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class TravelResult:
    """Represents the result of traveling to an NPC."""

    result: Literal["success", "not_a_valid_character"]
