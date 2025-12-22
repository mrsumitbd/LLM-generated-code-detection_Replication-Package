import os
import django
from django.conf import settings
from django.contrib.auth.models import User

def django_user_model(django_pglite_db: None) -> Any:
    """Pytest fixture providing Django's User model for testing.

    Args:
        django_pglite_db: Database fixture

    Returns:
        User model class
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
    django.setup()
    return User