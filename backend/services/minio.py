from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException
from config import settings
import io

class MinioService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(settings.MINIO_BUCKET_NAME):
                self.client.make_bucket(settings.MINIO_BUCKET_NAME)
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"MinIO initialization error: {str(e)}")
    
    async def upload_file(self, file_content: bytes, object_name: str) -> bool:
        try:
            self.client.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
                data=io.BytesIO(file_content),
                length=len(file_content),
                content_type='application/pdf'
            )
            return True
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    async def get_file(self, object_name: str) -> bytes:
        try:
            response = self.client.get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name
            )
            return response.read()
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")
    
    async def delete_file(self, object_name: str) -> bool:
        try:
            self.client.remove_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name
            )
            return True
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
    
    def get_presigned_url(self, object_name: str, expires: int = 3600) -> str:
        try:
            return self.client.presigned_get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=object_name,
                expires=expires
            )
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"URL generation failed: {str(e)}")

minio_service = MinioService()