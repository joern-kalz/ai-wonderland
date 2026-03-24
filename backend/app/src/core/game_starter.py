"""Logic for starting a new game session."""

import secrets

from src.adapters.ai.image_model import generate_png_image
from src.adapters.storage.session_store import write_session
from src.core.overview_generator import generate_overview
from src.model.game_session import GameSession
from src.model.npc import Npc


def start_game_and_return_session_token() -> str:
    """Starts a new game session."""

    overview = generate_overview()
    npc = overview.current_npc

    session = GameSession(
        crisis=overview.crisis,
        quests=overview.quests,
        actions_since_quest_start=0,
        current_npc=overview.current_npc,
        npcs_by_name={
            overview.current_npc: Npc(
                image=generate_png_image(overview.current_npc),
                chat_history=[],
            )
        },
        log=[overview.log],
    )

    sessionToken = secrets.token_urlsafe(32)
    write_session(sessionToken, session)
    return sessionToken
