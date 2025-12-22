from alembic import op

def upgrade() -> None:
    """
    Migration upgrade that adds a new enum value 'user' to the
    envstoreentity type. The commit is executed first to avoid
    the "unsafe use of new value" error that can occur when
    adding a value to an enum type inside a transaction.
    """
    # Commit the current transaction to avoid unsafe enum modification
    op.execute("COMMIT")

    # Add the new enum value
    op.execute("ALTER TYPE envstoreentity ADD VALUE 'user'")