def upgrade() -> None:
    from django.db import transaction
    from django.contrib.auth.models import User
    from myapp.models import EnvStoreEntity

    with transaction.atomic():
        for user in User.objects.all():
            user.envstoreentity_set.update(entity_type=EnvStoreEntity.EntityType.USER)