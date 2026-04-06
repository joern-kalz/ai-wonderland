"""Lambda handler for FastAPI app using Mangum."""

from mangum import Mangum
from src.adapters.api.fast_api_app import create_app


app = create_app()
handler = Mangum(app)
