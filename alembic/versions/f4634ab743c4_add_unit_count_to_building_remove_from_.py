"""Add unit_count to building, remove from property.

Revision ID: f4634ab743c4
Revises: 0e2c4df2ad81
Create Date: 2024-09-18 14:33:23.912965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4634ab743c4'
down_revision: Union[str, None] = '0e2c4df2ad81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buildings', sa.Column('unit_count', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_buildings_unit_count'), 'buildings', ['unit_count'], unique=False)
    op.alter_column('properties', 'city',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('properties', 'state',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('properties', 'zip_code',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_index('ix_properties_unit_count', table_name='properties')
    op.drop_column('properties', 'unit_count')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('properties', sa.Column('unit_count', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_index('ix_properties_unit_count', 'properties', ['unit_count'], unique=False)
    op.alter_column('properties', 'zip_code',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('properties', 'state',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('properties', 'city',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_buildings_unit_count'), table_name='buildings')
    op.drop_column('buildings', 'unit_count')
    # ### end Alembic commands ###
