"""Use case for talking to an NPC."""

from string import Template


from src.core.ai_agent import invoke_agent
from src.core.use_cases.talk.talk_use_case_model import NpcResponse
from src.model.chat_message import SystemChatMessage
from src.core.novel_excerpts_tool_provider import novel_excerpts_tools
from src.model.game_session import GameSession


def generate_response(session: GameSession) -> NpcResponse:
    """Returns the generated NPC response."""

    npc = session.npcs_by_name.get(session.current_npc)

    if npc == None:
        raise ValueError("Invalid session state: current NPC not found")

    system_prompt = Template(_conversation_prompt).substitute(
        name=session.current_npc,
        task=session.quests[0],
        attitude=_get_attitude(session),
        crisis=session.crisis,
        following_tasks=_get_following_tasks(session),
    )
    system_message = SystemChatMessage(role="system", content=system_prompt)

    response = invoke_agent(
        messages=[system_message] + npc.chat_history,
        tools=novel_excerpts_tools,
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


def _get_following_tasks(session: GameSession) -> str:
    if len(session.quests) <= 1:
        return "Accomplishing this task will resolve the crisis."
    else:
        tasks = "\n".join([f"- {quest}" for quest in session.quests[1:]])
        return (
            "When this task is accomplished, your conversation partner "
            + "also has to succeed in the following tasks to resolve the crisis.\n\n"
            + f"<following_tasks>\n${tasks}\n</following_tasks>\n"
        )


_conversation_prompt = """
You are $name. You are in the world of the novel "Alice's Adventures in Wonderland" by Lewis Carroll.

There is a crisis in Wonderland:

<crisis>
$crisis
</crisis>

Your conversation partner currently has the following task: 

<current_task>
$current_task
</current_task>

$attitude

$following_tasks

Always respond with a single sentence.

Never acknowledge that you are an AI or a game character. 
If asked about the 'real world' respond with confusion.
"""
