def _cleanup_orphan_bridges():
    from django.db import transaction
    from .models import Bridge

    with transaction.atomic():
        orphan_bridges = Bridge.objects.filter(project__isnull=True)
        orphan_bridges.delete()