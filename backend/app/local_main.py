from src.adapters.api.fast_api_app import create_app
from fastapi.middleware.cors import CORSMiddleware


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
