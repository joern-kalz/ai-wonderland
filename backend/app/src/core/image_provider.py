"""Provider of NPC images"""

from src.adapters.session_store import read_session
from src.core.image_generator import generate_npc_image


def provide_current_npc_image(session_token: str) -> bytes:
    """Provider of an image showing the current NPC"""

    session = read_session(session_token)
    npc = session.npcs_by_name.get(session.current_npc)

    if npc == None:
        npc.image = generate_npc_image(session.current_npc)
        npc.chat_history = []

    return npc.image
