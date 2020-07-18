"""Removing country.

Revision ID: bcbbfca74524
Revises: bdebd07fc4af
Create Date: 2020-07-18 20:23:20.093703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcbbfca74524'
down_revision = 'bdebd07fc4af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'country')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('country', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
