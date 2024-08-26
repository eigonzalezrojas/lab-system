"""Aumentar tamaño de la columna password_hash

Revision ID: b52b29d0e6cf
Revises: 2e569027bd04
Create Date: 2024-08-26 03:50:31.401507

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b52b29d0e6cf'
down_revision = '2e569027bd04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_accounts', 'password_hash',
               existing_type=mysql.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_accounts', 'password_hash',
               existing_type=sa.String(length=256),
               type_=mysql.VARCHAR(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###
