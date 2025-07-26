"""create animals table

Revision ID: a8d5432e9afc
Revises: 
Create Date: 2025-07-26 14:38:17.828316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8d5432e9afc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'animals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('animals')
