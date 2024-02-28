"""added new model objects

Revision ID: fe36ab5a33f4
Revises: 5d0a19060366
Create Date: 2024-02-28 14:25:49.033648

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'fe36ab5a33f4'
down_revision: Union[str, None] = '5d0a19060366'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('objects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('location', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('links', postgresql.ARRAY(sa.String()), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('objects')
    # ### end Alembic commands ###
