"""Use case for traveling to an NPC."""

from src.adapters.storage.session_store import read_session, write_session
from src.core.shared.image_generator import generate_npc_image
from src.core.use_cases.travel.npc_evaluator import map_npc
from src.model.npc import Npc
from src.model.travel_result import TravelResult


def travel(session_token: str, npc: str) -> TravelResult:
    """Travel to an NPC."""

    session = read_session(session_token)

    if session is None:
        raise ValueError("Invalid session token")

    mapping = map_npc(session, npc)
    session.log.append(mapping.log)

    if mapping.npc is None:
        write_session(session_token, session)
        return TravelResult(result="not_a_valid_character")

    if mapping.npc not in session.npcs_by_name:
        npc_image = generate_npc_image(mapping.npc)
        session.npcs_by_name[mapping.npc] = Npc(image=npc_image.image, chat_history=[])
        session.log.append(npc_image.log)

    session.current_npc = mapping.npc
    write_session(session_token, session)
    return TravelResult(result="success")
