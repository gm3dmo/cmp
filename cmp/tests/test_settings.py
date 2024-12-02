from django.test.runner import DiscoverRunner
from django.conf import settings
from pathlib import Path
import os
from core.settings import *  # Import all settings from core

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class NoStaticFilesRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        settings.STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# Required for CSRF
SECRET_KEY = 'dummy-key-for-tests'

# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Debug setting
DEBUG = True

# Override static files storage to use simple storage instead of compressed manifest
STORAGES = {
    "default": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}