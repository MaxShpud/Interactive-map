"""deleted UUID field

Revision ID: e9eb5d72c883
Revises: eaa1ef232053
Create Date: 2024-02-10 16:36:25.839052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9eb5d72c883' 
down_revision: Union[str, None] = 'eaa1ef232053'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'user_uuid')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_uuid', sa.UUID(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
