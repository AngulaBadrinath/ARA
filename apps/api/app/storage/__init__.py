"""S3-compatible object storage client."""

import boto3
import botocore
from botocore.config import Config

from app.core.config import get_settings


class StorageClient:
    """Wraps boto3 for MinIO / S3."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = boto3.client(
            "s3",
            endpoint_url=self.settings.s3_endpoint,
            aws_access_key_id=self.settings.s3_access_key,
            aws_secret_access_key=self.settings.s3_secret_key,
            region_name=self.settings.s3_region,
            use_ssl=self.settings.s3_use_ssl,
            config=Config(signature_version="s3v4"),
        )

    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.settings.s3_bucket)
        except botocore.exceptions.ClientError:
            self.client.create_bucket(Bucket=self.settings.s3_bucket)

    def generate_presigned_upload_url(self, storage_key: str, content_type: str) -> str:
        return self.client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.settings.s3_bucket,
                "Key": storage_key,
                "ContentType": content_type,
            },
            ExpiresIn=3600,
        )

    def get_object_bytes(self, storage_key: str) -> bytes:
        response = self.client.get_object(
            Bucket=self.settings.s3_bucket,
            Key=storage_key,
        )
        return response["Body"].read()
