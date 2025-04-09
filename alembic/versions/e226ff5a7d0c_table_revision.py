"""table revision

Revision ID: e226ff5a7d0c
Revises: 26348048e25d
Create Date: 2025-04-09 15:22:52.277704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e226ff5a7d0c'
down_revision: Union[str, None] = '26348048e25d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tables', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tables', type_='unique')
    # ### end Alembic commands ###
