"""Use case for traveling to an NPC."""

from src.adapters.storage.session_store import read_session, write_session
from src.core.use_cases.travel.npc_evaluator import map_npc
from src.model.travel_result import TravelResult


def travel(session_token: str, npc: str) -> TravelResult:
    """Travel to an NPC."""

    session = read_session(session_token)

    if session is None:
        raise ValueError("Invalid session token")

    mapping = map_npc(session, npc)

    if mapping.npc is None:
        return TravelResult(result="not_a_valid_character")

    session.current_npc = mapping.npc
    session.log.append(mapping.log)
    write_session(session_token, session)

    return TravelResult(result="success")
