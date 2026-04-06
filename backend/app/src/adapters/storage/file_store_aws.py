"""AWS S3 storage operations."""

import os
import boto3
from botocore.exceptions import ClientError


_s3_bucket = os.environ.get("S3_BUCKET")
_s3 = boto3.client("s3")


def read_text(filename: str) -> str | None:
    """Reads text from S3. Returns None if object not found."""
    return read_bytes(filename).decode("utf-8")


def write_text(filename: str, value: str) -> None:
    """Writes text to S3."""
    write_bytes(filename, value.encode("utf-8"))


def read_bytes(filename: str) -> bytes:
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
