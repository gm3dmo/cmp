import os
import django
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.conf import settings

def create_test_user():
    # Get the custom user model
    User = get_user_model()

    # Get credentials from Django settings (which gets them from .env)
    username = os.environ.get('admin_user')
    password = os.environ.get('admin_password')

    if not username or not password:
        print("Error: admin_user and admin_password must be set in .env file")
        sys.exit(1)

    try:
        # Create user if it doesn't exist, otherwise update password
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        if created:
            print(f"Created new superuser '{username}' with the specified password")
        else:
            print(f"Updated password for existing user '{username}'")

    except Exception as e:
        print(f"Error creating/updating user: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_test_user() 