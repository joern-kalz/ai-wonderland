"""API endpoint for starting a new game."""

import io

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from src.core.image_provider import provide_current_npc_image
from typing import Annotated
from fastapi import APIRouter, Header

image_router = APIRouter()


@image_router.get("/image")
async def get_image(x_session_token: Annotated[str, Header()]):
    """Returns an image of the current NPC."""

    image_bytes = provide_current_npc_image(x_session_token)
    image_stream = io.BytesIO(image_bytes)
    return StreamingResponse(image_stream, media_type="image/png")
