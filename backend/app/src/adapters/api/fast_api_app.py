"""Creates and configures the FastAPI application."""

from fastapi import FastAPI

from .start_game_endpoint import router as start_game_router


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""

    app = FastAPI()

    app.include_router(start_game_router)

    return app
