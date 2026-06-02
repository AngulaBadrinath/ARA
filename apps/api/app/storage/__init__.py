"""S3-compatible object storage client."""

from app.core.config import get_settings


class StorageClient:
    """Wraps boto3 for MinIO / S3. Implement upload URL and file retrieval."""

    def __init__(self) -> None:
        self.settings = get_settings()

    def ensure_bucket(self) -> None:
        """Create bucket if it does not exist."""
        pass

    def generate_presigned_upload_url(self, storage_key: str, content_type: str) -> str:
        """Return a presigned PUT URL for direct client upload."""
        raise NotImplementedError

    def get_object_bytes(self, storage_key: str) -> bytes:
        """Fetch object contents for worker text extraction."""
        raise NotImplementedError
