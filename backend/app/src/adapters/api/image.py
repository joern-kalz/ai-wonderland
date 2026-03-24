"""API endpoint for starting a new game."""

from fastapi import APIRouter, Response
from src.core.image_provider import provide_current_npc_image
from typing import Annotated
from fastapi import APIRouter, Header

image_router = APIRouter()


@image_router.get(
    "/image", responses={200: {"content": {"image/png": {}}}}, response_class=Response
)
async def get_image(x_session_token: Annotated[str, Header()]):
    """Returns an image of the current NPC."""

    image_bytes = provide_current_npc_image(x_session_token)
    return Response(content=image_bytes, media_type="image/png")
