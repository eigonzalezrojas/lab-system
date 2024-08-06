"""Change fondo to float in Project

Revision ID: be937ce11839
Revises: e8cf80b3854e
Create Date: 2024-08-06 02:51:20.868581

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'be937ce11839'
down_revision = 'e8cf80b3854e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'fondo',
               existing_type=mysql.VARCHAR(length=64),
               type_=sa.Float(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('projects', 'fondo',
               existing_type=sa.Float(),
               type_=mysql.VARCHAR(length=64),
               existing_nullable=False)
    # ### end Alembic commands ###