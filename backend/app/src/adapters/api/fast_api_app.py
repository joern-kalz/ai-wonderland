"""Creates and configures the FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.adapters.ai.text_to_text_model import initialize_text_to_text_model
from src.adapters.config.config_loader import load_config
from src.adapters.ai.image_model import initialize_image_model
from .start import start_router
from .image import image_router
from .talk import talk_router
from .travel import travel_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context for initialization."""
    load_config()
    initialize_image_model()
    initialize_text_to_text_model()
    yield


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""

    app = FastAPI(lifespan=lifespan)
    app.include_router(start_router)
    app.include_router(image_router)
    app.include_router(talk_router)
    app.include_router(travel_router)
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
