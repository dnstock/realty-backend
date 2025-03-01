"""Add columns to buildings table.

Revision ID: 179b091dbc20
Revises: 0b68bad72e35
Create Date: 2024-12-17 19:35:08.223012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '179b091dbc20'
down_revision: Union[str, None] = '0b68bad72e35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('buildings', schema=None) as batch_op:
        batch_op.add_column(sa.Column('floor_count', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('has_elevator', sa.Boolean(), server_default='false', nullable=False))
        batch_op.add_column(sa.Column('has_pool', sa.Boolean(), server_default='false', nullable=False))
        batch_op.add_column(sa.Column('has_gym', sa.Boolean(), server_default='false', nullable=False))
        batch_op.add_column(sa.Column('has_parking', sa.Boolean(), server_default='false', nullable=False))
        batch_op.add_column(sa.Column('has_doorman', sa.Boolean(), server_default='false', nullable=False))
        batch_op.drop_index('ix_buildings_unit_count')

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('buildings', schema=None) as batch_op:
        batch_op.create_index('ix_buildings_unit_count', ['unit_count'], unique=False)
        batch_op.drop_column('has_doorman')
        batch_op.drop_column('has_parking')
        batch_op.drop_column('has_gym')
        batch_op.drop_column('has_pool')
        batch_op.drop_column('has_elevator')
        batch_op.drop_column('floor_count')

    # ### end Alembic commands ###
