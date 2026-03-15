"""Adapter for the image generation model"""

import base64

from openai import OpenAI


def generate_png_image(prompt: str) -> bytes:
    result = _client.images.generate(
        model="gpt-image-1-mini", prompt=prompt, quality="low"
    )
    image_base64 = result.data[0].b64_json
    return base64.b64decode(image_base64)


_client = OpenAI()
