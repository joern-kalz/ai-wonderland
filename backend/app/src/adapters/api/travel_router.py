"""API endpoint for traveling with an NPC."""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from src.core.use_cases.travel.travel_use_case import travel

travel_router = APIRouter()


class TravelRequest(BaseModel):
    """Request for traveling to an NPC."""

    npc: str = Field(description="Name of the NPC to travel to")


@travel_router.post(
    "/travel",
    responses={
        400: {
            "description": "Not a valid character",
        }
    },
)
async def post_travel(
    x_session_token: Annotated[str, Header()], request: TravelRequest
) -> None:
    """Travels to an NPC."""

    result = travel(session_token=x_session_token, npc=request.npc)
    if result.result == "not_a_valid_character":
        raise HTTPException(status_code=400, detail={"error": "not_a_valid_character"})
