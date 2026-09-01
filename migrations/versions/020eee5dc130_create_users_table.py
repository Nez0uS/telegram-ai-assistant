"""create users table

Revision ID: 020eee5dc130
Revises: 83cc88c358e4
Create Date: 2026-09-01 18:00:22.518422

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '020eee5dc130'
down_revision: Union[str, Sequence[str], None] = '83cc88c358e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
