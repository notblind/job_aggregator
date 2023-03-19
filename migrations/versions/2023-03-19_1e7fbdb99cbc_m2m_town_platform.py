"""m2m town platform

Revision ID: 1e7fbdb99cbc
Revises: fd6ba02310c0
Create Date: 2023-03-19 16:35:22.926586

"""
import sqlalchemy as sa
from alembic import op

revision = '1e7fbdb99cbc'
down_revision = 'fd6ba02310c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('vacancies_association_town_platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('town_id', sa.Integer(), nullable=False),
    sa.Column('platform_id', sa.Integer(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['platform_id'], ['vacancies_platform.id'], ),
    sa.ForeignKeyConstraint(['town_id'], ['vacancies_town.id'], ),
    sa.PrimaryKeyConstraint('id', 'town_id', 'platform_id')
    )
    op.drop_column('vacancies_town', 'id_hh')


def downgrade() -> None:
    op.add_column('vacancies_town', sa.Column('id_hh', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_table('vacancies_association_town_platform')
