"""API endpoint for starting a new game."""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.core.use_cases.start.start_use_case import start_game_and_return_session_token

start_router = APIRouter()


class StartGameResponse(BaseModel):
    """Response for starting a new game."""

    session_token: str = Field(description="Secret session token for the game")


@start_router.post("/start")
async def post_start_game() -> StartGameResponse:
    """Starts a new game and returns the initial game state."""

    session_token = start_game_and_return_session_token()
    return StartGameResponse(session_token=session_token)
