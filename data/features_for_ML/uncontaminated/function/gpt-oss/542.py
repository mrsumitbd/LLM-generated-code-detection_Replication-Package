from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Create a simple example table
    op.create_table(
        "example",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
    )