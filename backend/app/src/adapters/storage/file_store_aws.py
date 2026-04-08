"""AWS S3 storage operations."""

import os
import boto3
from botocore.exceptions import ClientError

from src.adapters.config.global_config_provider import is_on_aws


_s3_bucket = os.environ.get("S3_BUCKET")

if is_on_aws():
    _s3 = boto3.client("s3")


def read_text(filename: str) -> str | None:
    """Reads text from S3. Returns None if object not found."""
    bytes_data = read_bytes(filename)
    return bytes_data.decode("utf-8") if bytes_data is not None else None


def write_text(filename: str, value: str) -> None:
    """Writes text to S3."""
    write_bytes(filename, value.encode("utf-8"))


def read_bytes(filename: str) -> bytes | None:
    """Reads bytes from S3."""
    try:
        return _s3.get_object(Bucket=_s3_bucket, Key=filename)["Body"].read()
    except ClientError as e:
        if e.response["Error"]["Code"] == "NoSuchKey":
            return None
        raise


def write_bytes(filename: str, value: bytes) -> None:
    """Writes bytes to S3."""
    _s3.put_object(Bucket=_s3_bucket, Key=filename, Body=value)
