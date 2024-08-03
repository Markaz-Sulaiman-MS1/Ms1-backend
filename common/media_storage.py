from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    bucket_name = settings.S3_BUCKET_NAME
    custom_domain = bucket_name
    location = "media"
