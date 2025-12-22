import os
import django
from django.db import connection, migrations

def check_if_migration_is_needed():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM django_migrations;")
            applied_migrations = [row[0] for row in cursor.fetchall()]
    except:
        applied_migrations = []

    unapplied_migrations = []
    for app in django.apps.get_app_configs():
        migration_module = f"{app.name}.migrations"
        if hasattr(django.apps.get_app_config(app.label), 'migrations'):
            for migration in django.apps.get_app_config(app.label).migrations.__all__:
                if migration not in applied_migrations:
                    unapplied_migrations.append(migration)

    return bool(unapplied_migrations)