import json
from string import Template

from dataclasses import dataclass
from pydantic import BaseModel

from src.adapters.ai.text_to_text_model import invoke_text_to_text_model
from src.model.chat_message import ChatMessage, UserChatMessage
from src.model.game_session import GameSession


@dataclass
class MappingResult:
    """Represents the result of mapping to an npc."""

    npc: str | None
    log: list[ChatMessage]


def map_npc(session: GameSession, npc_name: str) -> MappingResult:
    """Maps the npc_name to an npc if possible."""

    if not all(c.isalpha() or c in " -'" for c in npc_name):
        return MappingResult(npc=None, log=[])

    known_characters = [f"- ${c}" for c in session.npcs_by_name.keys()]
    prompt = Template(_prompt).substitute(
        input=npc_name, known_characters="\n".join(known_characters)
    )
    messages: list[ChatMessage] = [UserChatMessage(role="user", content=prompt)]

    raw_response = invoke_text_to_text_model(messages=messages, json_response=True)
    messages.append(raw_response)
    response = _Response.model_validate(json.loads(raw_response.content))

    if response.is_character_name == False:
        npc = None
    elif response.refers_to_known_character is not None:
        npc = response.refers_to_known_character
    else:
        npc = npc_name

    return MappingResult(
        npc=npc,
        log=messages,
    )


_prompt = """
Evaluate the following input:

<input>
$input
</input>

Check if the input is a possible name for a character in a book.

Check if the input refers to one of the following known characters:

<known_characters>
$known_characters
</known_characters>

Respond ONLY with valid JSON in the following format:

{
    "reasoning": "brief explanation of the evaluation",
    "is_character_name": "boolean (true if the input is a possible name for a character in a book, false otherwise)",
    "refers_to_known_character": "name of the known character the input refers to, or null if it does not refer to any known character",
}
"""


class _Response(BaseModel):
    """The response from the LLM."""

    reasoning: str
    is_character_name: bool
    refers_to_known_character: str | None
