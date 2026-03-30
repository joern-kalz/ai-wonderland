from pathlib import Path


def get_cache_path(cache_key: str) -> Path:
    """Returns the path to the cache file for the given key."""
    cache_dir = Path(__file__).parent / ".cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / f"{cache_key}"
