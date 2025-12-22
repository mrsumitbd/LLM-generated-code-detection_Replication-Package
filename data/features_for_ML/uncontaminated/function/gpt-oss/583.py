from typing import Any
from django.contrib.auth import get_user_model

def django_user_model(django_pglite_db: None) -> Any:
    """Pytest fixture providing Django's User model for testing.

    Args:
        django_pglite_db: Database fixture

    Returns:
        User model class
    """
    # The database fixture ensures Django is configured and the test DB is ready.
    # Simply return the User model class.
    return get_user_model()