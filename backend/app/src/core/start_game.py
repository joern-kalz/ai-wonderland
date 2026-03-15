"""Logic for starting a new game session."""

import generate_overview
from src.model.game_session import GameSession


def start_game() -> GameSession:
    """Starts a new game session."""

    overview = generate_overview()

    return GameSession(
        crisis=overview.crisis,
        quests=overview.quests,
        actions_since_quest_start=0,
        current_npc=overview.current_npc,
        npcs_by_name={},
    )
