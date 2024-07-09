"""Create tables

Revision ID: 0f7ff8588ea5
Revises: 
Create Date: 2024-07-09 01:27:51.563571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f7ff8588ea5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('maquinas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('muestras',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=False),
    sa.Column('mg', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('preparaciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proyectos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('solventes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('experimentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=64), nullable=False),
    sa.Column('solvente_id', sa.Integer(), nullable=False),
    sa.Column('preparacion_id', sa.Integer(), nullable=False),
    sa.Column('muestra_id', sa.Integer(), nullable=False),
    sa.Column('observacion', sa.Text(), nullable=True),
    sa.Column('recuperacionMuestra', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['muestra_id'], ['muestras.id'], ),
    sa.ForeignKeyConstraint(['preparacion_id'], ['preparaciones.id'], ),
    sa.ForeignKeyConstraint(['solvente_id'], ['solventes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('solicitudes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('proyecto_id', sa.Integer(), nullable=False),
    sa.Column('maquina_id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.Column('estado', sa.String(length=64), nullable=False),
    sa.Column('valor', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['maquina_id'], ['maquinas.id'], ),
    sa.ForeignKeyConstraint(['proyecto_id'], ['proyectos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('rut', sa.String(length=12), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id', 'rut'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('rut')
    )
    op.create_table('facturas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_nombre', sa.String(length=64), nullable=False),
    sa.Column('usuario_apellido', sa.String(length=64), nullable=False),
    sa.Column('usuario_rut', sa.String(length=12), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.Column('monto', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_rut'], ['users.rut'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('facturas')
    op.drop_table('users')
    op.drop_table('solicitudes')
    op.drop_table('experimentos')
    op.drop_table('solventes')
    op.drop_table('roles')
    op.drop_table('proyectos')
    op.drop_table('preparaciones')
    op.drop_table('muestras')
    op.drop_table('maquinas')
    # ### end Alembic commands ###
