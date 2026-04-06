import os


_env = os.environ.get("env", "local").strip().lower()


def is_on_aws() -> bool:
    """Determines whether to use AWS or local file storage."""
    return _env == "aws"
