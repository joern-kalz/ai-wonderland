"""Use case for talking to an NPC."""

from src.adapters.storage.session_store import read_session, write_session
from src.core.use_cases.talk.quest_evaluator import evaluate_current_quest
from src.core.use_cases.talk.response_generator import generate_response
from src.model.chat_message import UserChatMessage
from src.model.talk_result import TalkResult


def talk(session_token: str, message: str) -> TalkResult:
    """Talks to an NPC and returns the response."""

    session = read_session(session_token)

    if session is None:
        raise ValueError("Invalid session token")

    npc = session.npcs_by_name.get(session.current_npc)

    if npc == None:
        raise ValueError("Invalid session state: current NPC not found")

    npc.chat_history.append(UserChatMessage(role="user", content=message))

    response = generate_response(session)
    npc.chat_history.append(response.message)
    session.log.append(response.log)
    session.actions_since_quest_start += 1

    evaluation = evaluate_current_quest(session)
    session.log.append(evaluation.log)

    if evaluation.success:
        session.current_quest += 1
        session.actions_since_quest_start = 0

    write_session(session_token, session)

    return TalkResult(
        message=response.message.content,
        game_end=session.current_quest == len(session.quests),
    )
