def django_user_model(django_pglite_db: None) -> Any:
    from django.contrib.auth.models import User
    return User