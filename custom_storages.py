from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# Setup configuration adapted from Boutique Ado, where the settings used
# were identical to what was used in this project


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
