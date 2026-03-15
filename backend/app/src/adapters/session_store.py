"""GameSession persistence for game sessions."""

import os
from dataclasses import asdict
from src.model.game_session import GameSession

_sessions: dict[str, GameSession] = {}


def read_session(session_token: str) -> GameSession | None:
    """Retrieves a session by its token."""
    return _sessions.get(session_token)


def write_session(session_token: str, session: GameSession) -> None:
    """Saves a session by its token."""
    _sessions[session_token] = session
