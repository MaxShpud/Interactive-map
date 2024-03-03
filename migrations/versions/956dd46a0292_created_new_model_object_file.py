"""created new model object file

Revision ID: 956dd46a0292
Revises: bbb0340cd963
Create Date: 2024-03-03 16:08:50.404962

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '956dd46a0292'
down_revision: Union[str, None] = 'bbb0340cd963'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('objects_files',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['file_id'], ['files.id'], ),
    sa.ForeignKeyConstraint(['object_id'], ['objects.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('objects_files')
    # ### end Alembic commands ###