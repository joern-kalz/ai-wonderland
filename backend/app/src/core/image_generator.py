"""Application logic for creating images of NPCs"""

from src.adapters.ai.image_model import generate_png_image
from src.core.image_description_generator import generate_image_description


def generate_npc_image(npc: str) -> bytes:
    """Generates an image of the NPC"""

    response = generate_image_description(npc)
    prompt = response[-1].content
    return generate_png_image(prompt)
