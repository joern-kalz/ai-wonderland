from src.adapters.config.config_loader import load_config

load_config()

from src.adapters.api.fast_api_app import create_local_app

app = create_local_app()
