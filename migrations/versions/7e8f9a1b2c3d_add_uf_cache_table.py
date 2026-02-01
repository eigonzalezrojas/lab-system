"""Add uf_cache table for UF value caching

Revision ID: 7e8f9a1b2c3d
Revises: 6cb55872ca58
Create Date: 2026-02-01 12:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e8f9a1b2c3d'
down_revision = '6cb55872ca58'
branch_labels = None
depends_on = None


def upgrade():
    # Crear tabla uf_cache
    op.create_table('uf_cache',
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('valor', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('fecha')
    )


def downgrade():
    # Eliminar tabla uf_cache
    op.drop_table('uf_cache')
