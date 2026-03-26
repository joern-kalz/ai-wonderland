import json
from string import Template

from pydantic import BaseModel

from src.adapters.ai.text_to_text_model import invoke_text_to_text_model
from src.core.use_cases.talk.talk_use_case_model import EvaluationResult
from src.model.chat_message import ChatMessage, UserChatMessage
from src.model.game_session import GameSession


def evaluate_current_quest(session: GameSession) -> EvaluationResult:
    """Evaluates the player's success in the current quest."""

    chat = "\n".join(
        [
            f"{"Player" if message.role == "user" else session.current_npc}: {message.content}"
            for message in session.npcs_by_name[session.current_npc].chat_history
        ]
    )

    prompt = Template(_evaluation_prompt).substitute(
        name=session.current_npc,
        task=session.quests[session.current_quest],
        chat=chat,
    )

    messages: list[ChatMessage] = [UserChatMessage(role="user", content=prompt)]
    raw_response = invoke_text_to_text_model(messages=messages, json_response=True)
    messages += [raw_response]

    response = json.loads(raw_response.content)
    success = response["success"] == True or (
        isinstance(response["success"], str) and response["success"].lower() == "true"
    )
    return EvaluationResult(success=success, log=messages)


_evaluation_prompt = """
The player in a game has the following task:

<task>
$task
</task>

Evaluate the player's success on this task 
based on the following conversation with $name:

<chat>
$chat
</chat>

Respond ONLY with valid JSON in the following format:

{
    "success": "boolean (true if the player has succeeded on the task)",
    "reason": "brief explanation of the evaluation"
}
"""


class _Response(BaseModel):
    """The response from the LLM."""

    success: bool
    reason: str
