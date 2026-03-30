"""Adapter for the image generation model"""

import base64

from openai import OpenAI

_client: OpenAI | None = None


def initialize_image_model() -> None:
    """Initialize the image generation client."""
    global _client
    _client = OpenAI()


def generate_png_image(prompt: str) -> bytes:
    if _client is None:
        raise RuntimeError("Call initialize_image_model() before use.")

    result = _client.images.generate(
        model="gpt-image-1-mini", prompt=prompt, quality="low", size="1024x1024"
    )

    if result.data is None or len(result.data) == 0 or not result.data[0].b64_json:
        raise ValueError("No image data returned from the API")

    image_base64 = result.data[0].b64_json
    return base64.b64decode(image_base64)
