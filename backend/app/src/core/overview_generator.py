"""Generator of the game overview."""

import json

from pydantic import BaseModel

from src.adapters.ai.text_to_text_model import invoke_text_to_text_model
from src.model.game_overview import GameOverview
from src.model.chat_message import ChatMessage, UserChatMessage


def generate_overview() -> GameOverview:
    """Generates an overview of the game."""

    messages: list[ChatMessage] = [UserChatMessage(role="user", content=_prompt)]
    response = invoke_text_to_text_model(
        messages=messages,
    )
    messages += [response]

    print("Raw response from LLM:")
    print(messages)
    response = _Response.model_validate(json.loads(messages[-1].content))

    return GameOverview(
        crisis=response.crisis,
        quests=response.quests_to_resolve_crisis,
        current_npc=response.introduction_npc,
        log=messages,
    )


_prompt = """
You are a game writer.

Your task is to generate a walkthrough for an adventure game in the world of the 
novel "Alice's Adventures in Wonderland" by Lewis Carroll.

The goal of the game must be resolving a crisis. 

To resolve the crisis the player must have to take a series of
sequential quests by talking to NPCs.

The player starts without any knowledge of the crisis. Finding out
about the crisis must be included in the quests.

The quests should be logically connected. 
Completing one quests leads the player to the next quest.

Respond ONLY with valid JSON with the following format:

{
    "crisis": "Description of an existential crisis in the world of Wonderland",
    "introduction_npc": "The NPC at the start of the game",
    "quests_to_resolve_crisis": ["Quests the player must complete to resolve the crisis"]
}
"""


class _Response(BaseModel):
    """The response from the LLM."""

    crisis: str
    introduction_npc: str
    quests_to_resolve_crisis: list[str]


if __name__ == "__main__":
    print(generate_overview())
