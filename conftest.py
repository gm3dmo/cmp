import os
import pytest
from django.conf import settings
from django.core.management import call_command

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        test_static_dir = os.path.join(settings.BASE_DIR, 'test_static')
        if not os.path.exists(test_static_dir):
            os.makedirs(test_static_dir)
        call_command('collectstatic', '--noinput', '--clear') 