"""API endpoint for talking with an NPC."""

from typing import Annotated

from fastapi import APIRouter, Header
from pydantic import BaseModel, Field

from src.core.use_cases.talk.talk_use_case import talk

talk_router = APIRouter()


class TalkRequest(BaseModel):
    """Request for talking to an NPC."""

    message: str = Field(description="Message to send to the NPC")


class TalkResponse(BaseModel):
    """Response for talking to an NPC."""

    message: str = Field(description="Response from the NPC")
    game_end: bool = Field(description="True if the game is over")


@talk_router.post("/talk")
async def post_talk(
    x_session_token: Annotated[str, Header()], request: TalkRequest
) -> TalkResponse:
    """Talks to an NPC and returns the response."""

    result = talk(session_token=x_session_token, message=request.message)
    return TalkResponse(message=result.message, game_end=result.game_end)
