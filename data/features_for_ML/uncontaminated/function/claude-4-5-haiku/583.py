def django_user_model(django_pglite_db: None) -> Any:
    """Pytest fixture providing Django's User model for testing.

    Args:
        django_pglite_db: Database fixture

    Returns:
        User model class
    """
    from django.contrib.auth.models import User
    return User