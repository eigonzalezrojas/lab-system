"""Add samplePreparation and observation tables, update requests table

Revision ID: b39a553d1f4d
Revises: 9f9e37e0d295
Create Date: 2024-07-21 20:17:06.101653

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b39a553d1f4d'
down_revision = '9f9e37e0d295'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('observation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sample_preparation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('requests', sa.Column('user_rut', sa.String(length=12), nullable=False))
    op.add_column('requests', sa.Column('solvent_id', sa.Integer(), nullable=False))
    op.add_column('requests', sa.Column('sample_preparation_id', sa.Integer(), nullable=False))
    op.add_column('requests', sa.Column('sample_id', sa.Integer(), nullable=False))
    op.add_column('requests', sa.Column('fecha', sa.DateTime(), nullable=False))
    op.add_column('requests', sa.Column('request_name', sa.String(length=64), nullable=False))
    op.add_column('requests', sa.Column('price', sa.Float(), nullable=False))
    op.drop_constraint('requests_ibfk_1', 'requests', type_='foreignkey')
    op.create_foreign_key(None, 'requests', 'samples', ['sample_id'], ['id'])
    op.create_foreign_key(None, 'requests', 'solvents', ['solvent_id'], ['id'])
    op.create_foreign_key(None, 'requests', 'user_accounts', ['user_rut'], ['rut'])
    op.create_foreign_key(None, 'requests', 'sample_preparation', ['sample_preparation_id'], ['id'])
    op.drop_column('requests', 'value')
    op.drop_column('requests', 'date')
    op.drop_column('requests', 'status')
    op.drop_column('requests', 'machine_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requests', sa.Column('machine_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('requests', sa.Column('status', mysql.VARCHAR(length=64), nullable=False))
    op.add_column('requests', sa.Column('date', sa.DATE(), nullable=False))
    op.add_column('requests', sa.Column('value', mysql.FLOAT(), nullable=False))
    op.drop_constraint(None, 'requests', type_='foreignkey')
    op.drop_constraint(None, 'requests', type_='foreignkey')
    op.drop_constraint(None, 'requests', type_='foreignkey')
    op.drop_constraint(None, 'requests', type_='foreignkey')
    op.create_foreign_key('requests_ibfk_1', 'requests', 'machines', ['machine_id'], ['id'])
    op.drop_column('requests', 'price')
    op.drop_column('requests', 'request_name')
    op.drop_column('requests', 'fecha')
    op.drop_column('requests', 'sample_id')
    op.drop_column('requests', 'sample_preparation_id')
    op.drop_column('requests', 'solvent_id')
    op.drop_column('requests', 'user_rut')
    op.drop_table('sample_preparation')
    op.drop_table('observation')
    # ### end Alembic commands ###
