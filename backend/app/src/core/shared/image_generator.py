"""Application logic for creating images of NPCs"""

from src.adapters.ai.image_model import generate_png_image
from src.core.shared.image_description_generator import generate_image_description
from src.model.image_generation_result import ImageGenerationResult


def generate_npc_image(npc: str) -> ImageGenerationResult:
    """Generates an image of the NPC"""

    response = generate_image_description(npc)
    prompt = response[-1].content
    image = generate_png_image(prompt)

    return ImageGenerationResult(image=image, log=response)
