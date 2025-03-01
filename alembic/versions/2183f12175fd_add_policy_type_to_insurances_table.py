"""Add policy_type to insurances table

Revision ID: 2183f12175fd
Revises: a6021bc40686
Create Date: 2025-01-17 12:42:12.743430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2183f12175fd'
down_revision: Union[str, None] = 'a6021bc40686'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('insurances', schema=None) as batch_op:
        batch_op.add_column(sa.Column('policy_type', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('insurances', schema=None) as batch_op:
        batch_op.drop_column('policy_type')

    # ### end Alembic commands ###
