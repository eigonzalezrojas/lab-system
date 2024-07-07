"""Add password_hash to User

Revision ID: 91752bebb923
Revises: 
Create Date: 2024-07-07 23:16:42.223031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91752bebb923'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
