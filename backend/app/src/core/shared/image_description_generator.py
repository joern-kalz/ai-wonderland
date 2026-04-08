from string import Template

from src.adapters.ai.text_to_text_model import initialize_text_to_text_model
from src.core.shared.ai_agent import invoke_agent
from src.core.shared.novel_excerpts_retriever import initialize_novel_excerpts_retriever
from src.model.chat_message import ChatMessage, UserChatMessage
from src.core.shared.novel_excerpts_tool_provider import get_novel_excerpts_tools


def generate_image_description(npc: str) -> list[ChatMessage]:
    template = Template(_prompt_template)
    prompt = template.substitute(npc=npc)
    return invoke_agent(
        messages=[UserChatMessage(role="user", content=prompt)],
        tools=get_novel_excerpts_tools(),
        max_iterations=3,
    )


_prompt_template = """
Create a description of $npc and a suitable setting for a text-to-image LLM. 
$npc must be stationary and not moving.
The description must not mention any other character besides $npc.
Respond only with the description and do not include an introductory sentence.
"""

if __name__ == "__main__":
    initialize_text_to_text_model()
    initialize_novel_excerpts_retriever()
    while True:
        npc = input("NPC: ")
        print(generate_image_description(npc))
