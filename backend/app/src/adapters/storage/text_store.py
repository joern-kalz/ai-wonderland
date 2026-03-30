"""Caching of strings"""

from src.adapters.cache.cache_path_provider import get_cache_path


def write_text(key: str, value: str) -> None:
    """Sets the value for the cache key"""

    get_cache_path(key).write_text(value)


def read_text(key: str) -> str | None:
    """Retrieves the value for the cache key if it exists or None otherwise"""

    try:
        get_cache_path(key).read_text()
    except FileNotFoundError:
        return None
