from string import Template

from src.core.shared.ai_agent import invoke_agent
from src.model.chat_message import ChatMessage, UserChatMessage
from src.core.shared.novel_excerpts_tool_provider import novel_excerpts_tools


def generate_image_description(npc: str) -> list[ChatMessage]:
    template = Template(_prompt_template)
    prompt = template.substitute(npc=npc)
    return invoke_agent(
        messages=[UserChatMessage(role="user", content=prompt)],
        tools=novel_excerpts_tools,
        max_iterations=3,
    )


_prompt_template = """
Create a description of $npc and a suitable setting for a text-to-image LLM. 
$npc must be stationary and not moving.
The description must not mention any other character besides $npc.
Respond only with the description and do not include an introductory sentence.
"""
