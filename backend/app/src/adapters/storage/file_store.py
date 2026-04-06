from src.adapters.config.global_config_provider import is_on_aws
from src.adapters.storage import file_store_aws, file_store_local


def read_text(filename: str) -> str | None:
    """Reads text from storage (S3 or local based on environment)."""
    if is_on_aws():
        return file_store_aws.read_text(filename)
    else:
        return file_store_local.read_text(filename)


def write_text(filename: str, value: str) -> None:
    """Writes text to storage (S3 or local based on environment)."""
    if is_on_aws():
        file_store_aws.write_text(filename, value)
    else:
        file_store_local.write_text(filename, value)


def read_bytes(filename: str) -> bytes:
    """Reads bytes from storage (S3 or local based on environment)."""
    if is_on_aws():
        return file_store_aws.read_bytes(filename)
    else:
        return file_store_local.read_bytes(filename)


def write_bytes(filename: str, value: bytes) -> None:
    """Writes bytes to storage (S3 or local based on environment)."""
    if is_on_aws():
        file_store_aws.write_bytes(filename, value)
    else:
        file_store_local.write_bytes(filename, value)
