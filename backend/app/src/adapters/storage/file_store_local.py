"""Local file storage operations using the cache directory."""

from src.adapters.cache.cache_provider import get_cache_path


def read_text(filename: str) -> str | None:
    """Reads text from local cache file. Returns None if not found."""
    try:
        return get_cache_path(filename).read_text()
    except FileNotFoundError:
        return None


def write_text(filename: str, value: str) -> None:
    """Writes text to local cache file."""
    get_cache_path(filename).write_text(value)


def read_bytes(filename: str) -> bytes:
    """Reads bytes from local cache file."""
    return get_cache_path(filename).read_bytes()


def write_bytes(filename: str, value: bytes) -> None:
    """Writes bytes to local cache file."""
    get_cache_path(filename).write_bytes(value)
