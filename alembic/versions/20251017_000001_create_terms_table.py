"""create terms table

Revision ID: 20251017_000001
Revises: 
Create Date: 2025-10-17 00:00:01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '20251017_000001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'terms',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('keyword', sa.String(length=120), nullable=False),
        sa.Column('description', sa.String(length=4000), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint('uq_terms_keyword', 'terms', ['keyword'])
    op.create_index('ix_terms_keyword', 'terms', ['keyword'])


def downgrade() -> None:
    op.drop_index('ix_terms_keyword', table_name='terms')
    op.drop_constraint('uq_terms_keyword', 'terms', type_='unique')
    op.drop_table('terms')


