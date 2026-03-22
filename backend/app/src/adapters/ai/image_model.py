"""Adapter for the image generation model"""

import base64

from openai import OpenAI


def generate_png_image(prompt: str) -> bytes:
    result = _client.images.generate(
        model="gpt-image-1-mini", prompt=prompt, quality="low"
    )

    if result.data is None or len(result.data) == 0 or not result.data[0].b64_json:
        raise ValueError("No image data returned from the API")

    image_base64 = result.data[0].b64_json
    return base64.b64decode(image_base64)


_client = OpenAI()
