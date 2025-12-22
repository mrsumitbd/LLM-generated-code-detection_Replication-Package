from django.contrib.auth import get_user_model
from typing import Any

def django_user_model(django_pglite_db: None) -> Any:
    """Pytest fixture providing Django's User model for testing.

    Args:
        django_pglite_db: Database fixture

    Returns:
        User model class
    """
    if not HAS_DJANGO:
        raise ImportError(
            "Django is required for Django integration. "
            "Install with: pip install 'py-pglite[django]'"
        )

    from django.contrib.auth import get_user_model

    return get_user_model()