"""Loader for the app configuration"""

import os

import boto3
from dotenv import load_dotenv

from src.adapters.config.global_config_provider import is_on_aws


def load_config() -> None:
    """Loads the app configuration"""
    load_dotenv()

    if is_on_aws():
        load_key("OPENAI")
        load_key("GROQ")


def load_key(name: str) -> None:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=os.environ[f"{name}_SECRET_NAME"])
    os.environ[f"{name}_API_KEY"] = response["SecretString"]
