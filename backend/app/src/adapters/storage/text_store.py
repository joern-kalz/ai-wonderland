"""Caching of strings"""

from src.adapters.storage import file_store


def write_text(key: str, value: str) -> None:
    """Sets the value for the cache key"""

    file_store.write_text(key, value)


def read_text(key: str) -> str | None:
    """Retrieves the value for the cache key if it exists or None otherwise"""

    return file_store.read_text(key)
