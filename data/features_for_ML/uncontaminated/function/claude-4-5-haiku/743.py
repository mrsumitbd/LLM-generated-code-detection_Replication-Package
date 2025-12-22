def upgrade() -> None:
    # this needs to be commited first to avoid: unsafe use of new value "user" of enum type envstoreentity
    from alembic import op
    import sqlalchemy as sa
    
    # Add the new 'user' value to the envstoreentity enum type
    op.execute("ALTER TYPE envstoreentity ADD VALUE 'user'")