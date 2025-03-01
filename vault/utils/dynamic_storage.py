from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.deconstruct import deconstructible

from storages.backends.s3boto3 import S3Boto3Storage
from storages.backends.azure_storage import AzureStorage
from storages.backends.gcloud import GoogleCloudStorage
import uuid

@deconstructible
class DynamicStorage:
    """
    Dynamic storage class that switches between local and S3 storage
    based on configuration
    """
    @staticmethod
    def get_storage():
        """
        Returns the appropriate storage backend based on settings
        """
        storage_type = settings.STORAGE_TYPE
        
        if storage_type == 's3':
            return S3Boto3Storage(
                bucket_name=settings.STORAGE_CONFIG[storage_type]['AWS_STORAGE_BUCKET_NAME'],
                access_key=settings.STORAGE_CONFIG[storage_type]['AWS_ACCESS_KEY_ID'],
                secret_key=settings.STORAGE_CONFIG[storage_type]['AWS_SECRET_ACCESS_KEY'],
                region_name=settings.STORAGE_CONFIG[storage_type]['AWS_S3_REGION_NAME'],
            )
        elif storage_type == 'gcs':
            return GoogleCloudStorage(
                bucket_name=settings.STORAGE_CONFIG[storage_type]['GCS_BUCKET_NAME'],
                region_name=settings.STORAGE_CONFIG[storage_type]['GCS_REGION_NAME'],
                credentials=settings.STORAGE_CONFIG[storage_type]['GCS_CREDENTIALS_FILE'],
            )
        elif storage_type == 'azure':
            return AzureStorage(
                connection_string=settings.STORAGE_CONFIG[storage_type]['AZURE_STORAGE_CONNECTION_STRING'],
                container=settings.STORAGE_CONFIG[storage_type]['AZURE_STORAGE_CONTAINER'],
            )
        return FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        )

def get_upload_path(instance, filename):
    """
    Generates a unique name for the file to avoid conflicts with existing files
    Example: resume-1234567890.pdf
    """
    ext = filename.split('.')[-1]
    new_name = f"{uuid.uuid4()}.{ext}"
    return new_name
    