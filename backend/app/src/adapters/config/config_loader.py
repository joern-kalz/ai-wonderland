"""Loader for the app configuration"""

import os

from dotenv import load_dotenv


def load_config() -> None:
    print("Loading config...")
    load_dotenv()
    print(os.environ["OPENAI_API_KEY"])
