"""create food table

Revision ID: 5ec566d6cb98
Revises: a8d5432e9afc
Create Date: 2025-07-26 14:38:18.165277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ec566d6cb98'
down_revision: Union[str, Sequence[str], None] = 'a8d5432e9afc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'food',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('animal_id', sa.Integer, nullable=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

    op.create_foreign_key(
        "fk_food_animal",
        "food",
        "animals",
        ["animal_id"],
        ["id"],
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('food')
