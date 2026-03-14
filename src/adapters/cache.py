"""Caching of strings"""

from pathlib import Path


def write_to_cache(key: str, value: str) -> None:
    """Sets the value for the cache key"""

    file_path = Path(f"cache/{key}.txt")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(value)


def read_from_cache(key: str) -> str | None:
    """Retrieves the value for the cache key if it exists or None otherwise"""

    try:
        with open(f"cache/{key}.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
