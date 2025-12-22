from alembic import op

def upgrade() -> None:
    # this needs to be commited first to avoid: unsafe use of new value "user" of enum type envstoreentity
    with op.get_context().autocommit_block():
        op.execute("ALTER TYPE envstoreentity ADD VALUE 'user'")