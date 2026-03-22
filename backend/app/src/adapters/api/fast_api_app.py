"""Creates and configures the FastAPI application."""

from fastapi import FastAPI

from .start_game_endpoint import router as start_game_router
from .get_image_endpoint import image_router
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""

    app = FastAPI()
    app.include_router(start_game_router)
    app.include_router(image_router)
    return app


def create_local_app() -> FastAPI:
    """Creates and configures the FastAPI application for local development."""

    app = create_app()

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

    return app
