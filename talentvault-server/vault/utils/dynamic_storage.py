from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.deconstruct import deconstructible

import logging
import uuid

from storages.backends.s3boto3 import S3Boto3Storage
from storages.backends.azure_storage import AzureStorage

logger = logging.getLogger('vault.api')

@deconstructible
def get_storage():
    """
    Returns the appropriate storage backend based on settings
    """
    storage_type = settings.STORAGE_TYPE

    try:
        storage = None
        if storage_type == 's3':
            storage = S3Boto3Storage(
                bucket_name=settings.STORAGE_CONFIG[storage_type]['AWS_STORAGE_BUCKET_NAME'],
                access_key=settings.STORAGE_CONFIG[storage_type]['AWS_ACCESS_KEY_ID'],
                secret_key=settings.STORAGE_CONFIG[storage_type]['AWS_SECRET_ACCESS_KEY'],
                region_name=settings.STORAGE_CONFIG[storage_type]['AWS_S3_REGION_NAME'],
            )
        elif storage_type == 'azure':
            storage = AzureStorage(
                connection_string=settings.STORAGE_CONFIG[storage_type]['AZURE_STORAGE_CONNECTION_STRING'],
                azure_container=settings.STORAGE_CONFIG[storage_type]['AZURE_STORAGE_CONTAINER']
            )
        else:
            storage = FileSystemStorage(
                location=settings.STORAGE_CONFIG[storage_type]['MEDIA_ROOT'],
                base_url=settings.STORAGE_CONFIG[storage_type]['MEDIA_URL']
            )

        # Monkey patch the save method to add logging
        original_save = storage.save
        def save_with_logging(name, content, *args, **kwargs):
            try:    
                result = original_save(name, content, *args, **kwargs)
                logger.info(f"Successfully saved file {name} to {storage_type} storage")
                return result
            except Exception as e:
                logger.error(f"Error saving file {name} to {storage_type} storage: {str(e)}")
                raise
        storage.save = save_with_logging

        return storage

    except Exception as e:
        logger.error(f"Error initializing storage backend: {str(e)}")
        raise

def get_upload_path(instance, filename):
    """
    Generates a unique name for the file to avoid conflicts with existing files
    Example: resume-1234567890.pdf
    """
    ext = filename.split('.')[-1]
    new_name = f"{uuid.uuid4()}.{ext}"
    logger.info("File uploaded successfully")
    return new_name
    