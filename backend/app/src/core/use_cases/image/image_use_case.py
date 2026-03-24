"""Provider of NPC images"""

from src.adapters.storage.session_store import read_session


def provide_current_npc_image(session_token: str) -> bytes:
    """Provides an image showing the current NPC"""

    session = read_session(session_token)

    if session is None:
        raise ValueError("Invalid session token")

    npc = session.npcs_by_name.get(session.current_npc)

    if npc == None:
        raise ValueError("Invalid session state: current NPC not found")

    return npc.image
