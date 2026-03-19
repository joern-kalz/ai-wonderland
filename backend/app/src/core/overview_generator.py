"""Generator of the game overview."""

from pydantic import BaseModel

from src.adapters.llama import invoke_llama
from src.model.game_overview import GameOverview
from src.model.message import ChatMessage


def generate_overview() -> GameOverview:
    """Generates an overview of the game."""

    messages = [ChatMessage(role="system", content=_prompt)]

    raw_response = invoke_llama(messages=messages, temperature=1.1)
    response = _Response.model_validate(raw_response)

    return GameOverview(
        crisis=response.crisis,
        quests=response.quests_to_resolve_crisis,
        current_npc=response.introduction_npc,
    )


_prompt = """
Generate a walkthrough for an adventure game in the world of the 
novel "Alice's Adventures in Wonderland" by Lewis Carroll.

The goal of the game must be resolving a crisis. 

To resolve the crisis the player must have to take a series of
sequential quests the player has to fulfill by talking to NPCs.

The player starts without any knowledge of the crisis. Finding out
about the crisis must be included in the quests.

Each quests should be logically connected. 
Completing one quests leads the player to the next quest.

Respond ONLY with valid JSON.

Output Format:

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
