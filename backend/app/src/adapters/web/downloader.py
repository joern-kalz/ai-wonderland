"""Downloading files from the internet"""

import requests


def download_text(url):
    """Downloads the text content from a given URL."""

    response = requests.get(url)
    response.raise_for_status()
    return response.text
