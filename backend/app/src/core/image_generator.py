"""Application logic for creating images of NPCs"""

from src.adapters.image_model import generate_png_image
from src.core.image_description_generator import generate_image_description


def generate_npc_image(npc: str) -> bytes:
    """Generates an image of the NPC"""

    prompt = generate_image_description(npc)
    return generate_png_image(prompt)
