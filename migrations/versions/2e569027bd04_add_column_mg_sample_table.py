"""add column mg sample table

Revision ID: 2e569027bd04
Revises: 39cb81ee1584
Create Date: 2024-08-18 16:16:49.970584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e569027bd04'
down_revision = '39cb81ee1584'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('samples', sa.Column('miligramos', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('samples', 'miligramos')
    # ### end Alembic commands ###
