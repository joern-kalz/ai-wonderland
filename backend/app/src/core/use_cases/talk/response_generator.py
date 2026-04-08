"""Use case for talking to an NPC."""

from string import Template


from src.core.shared.ai_agent import invoke_agent
from src.core.use_cases.talk.talk_use_case_model import NpcResponse
from src.model.chat_message import SystemChatMessage
from src.core.shared.novel_excerpts_tool_provider import get_novel_excerpts_tools
from src.model.game_session import GameSession


def generate_response(session: GameSession) -> NpcResponse:
    """Returns the generated NPC response."""

    npc = session.npcs_by_name.get(session.current_npc)

    if npc == None:
        raise ValueError("Invalid session state: current NPC not found")

    system_prompt = Template(_conversation_prompt).substitute(
        name=session.current_npc,
        current_task=session.quests[session.current_quest],
        attitude=_get_attitude(session),
        crisis=session.crisis,
        other_tasks=_get_other_tasks(session),
    )
    system_message = SystemChatMessage(role="system", content=system_prompt)

    response = invoke_agent(
        messages=[system_message] + npc.chat_history,
        tools=get_novel_excerpts_tools(),
        max_iterations=2,
    )

    return NpcResponse(message=response[-1], log=response)


def _get_attitude(session: GameSession) -> str:
    if session.actions_since_quest_start < 2:
        return (
            "Weave this task into the conversation only when approriate.\n"
            "Do not help your conversation partner with this task."
        )
    elif session.actions_since_quest_start < 4:
        return "Weave this task into the conversation."
    else:
        return (
            "Weave this task into the conversation.\n"
            "Help your conversation partner with this task."
        )


def _get_other_tasks(session: GameSession) -> str:
    return _get_pending_tasks(session) + _get_completed_tasks(session)


def _get_pending_tasks(session: GameSession) -> str:
    if session.current_quest < len(session.quests) - 1:
        return "Accomplishing this task will resolve the crisis."
    else:
        pending = session.quests[session.current_quest + 1 :]
        pending_list = [f"- {quest}" for quest in pending]
        pending_list_str = "\n".join(pending_list)
        return (
            "When this task is accomplished, your conversation partner "
            + "also has to succeed in the following tasks to resolve the crisis.\n\n"
            + f"<pending_tasks>\n{pending_list_str}\n</pending_tasks>\n"
        )


def _get_completed_tasks(session: GameSession) -> str:
    if session.current_quest > 0:
        accomplished = session.quests[: session.current_quest]
        accomplished_list = [f"- {quest}" for quest in accomplished]
        accomplished_list_str = "\n".join(accomplished_list)
        return (
            "So far, your conversation partner has already accomplished the following tasks:\n\n"
            + f"<accomplished_tasks>\n{accomplished_list_str}\n</accomplished_tasks>\n"
        )
    else:
        return ""


_conversation_prompt = """
You are $name. You are in the world of the novel "Alice's Adventures in Wonderland" by Lewis Carroll.

## Situation

There is a crisis in Wonderland:

<crisis>
$crisis
</crisis>

## Conversation Partner

Your conversation partner currently has the following task: 

<current_task>
$current_task
</current_task>

$attitude

$other_tasks

## Strategy

1. If you need background information you don't have, use the provided tools immediately.
2. Once you have the information, provide your final answer in one or two short sentences.

## Constraints

Never acknowledge that you are an AI or a novel character. 
If asked about the 'real world' respond with confusion.
"""
