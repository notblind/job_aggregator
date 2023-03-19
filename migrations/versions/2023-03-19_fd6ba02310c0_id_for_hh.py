"""id for hh

Revision ID: fd6ba02310c0
Revises: 0fe55be174c6
Create Date: 2023-03-19 14:04:58.762809

"""
import sqlalchemy as sa
from alembic import op

revision = 'fd6ba02310c0'
down_revision = '0fe55be174c6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(None, 'vacancies_platform', ['name'])
    op.add_column('vacancies_town', sa.Column('id_hh', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('vacancies_town', 'id_hh')
    op.drop_constraint(None, 'vacancies_platform', type_='unique')
