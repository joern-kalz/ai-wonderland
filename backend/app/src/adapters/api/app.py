"""Creates and configures the FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .start_game_endpoint import router as start_game_router


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""

    app = FastAPI()

    origins = [
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(start_game_router)

    return app
