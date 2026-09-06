"""add foreign key to messages user

Revision ID: ebf01d76f221
Revises: 020eee5dc130
Create Date: 2026-09-04 16:53:27.902170

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ebf01d76f221"
down_revision: str | Sequence[str] | None = "020eee5dc130"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute(
        """
        UPDATE messages
        SET user_id = users.id
        FROM users
        WHERE messages.user_id = users.telegram_id
        """
    )

    op.create_foreign_key(
        "fk_messages_user_id", "messages", "users", ["user_id"], ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_messages_user_idmessages", type_="foreignkey", table_name="messages"
    )
