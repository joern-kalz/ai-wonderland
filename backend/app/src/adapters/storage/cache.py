"""Caching of strings"""

import os
from pathlib import Path


def write_to_cache(key: str, value: str) -> None:
    """Sets the value for the cache key"""

    file_path = Path(os.path.join(_cache_dir, f"{key}"))
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(value)


def read_from_cache(key: str) -> str | None:
    """Retrieves the value for the cache key if it exists or None otherwise"""

    try:
        with open(os.path.join(_cache_dir, f"{key}"), "r") as file:
            return file.read()
    except FileNotFoundError:
        return None


_module_dir = os.path.dirname(__file__)
_cache_dir = os.path.join(_module_dir, ".cache")
