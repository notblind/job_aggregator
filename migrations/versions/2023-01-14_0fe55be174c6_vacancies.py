"""Vacancies

Revision ID: 0fe55be174c6
Revises: 
Create Date: 2023-01-15 00:38:50.793415

"""
from alembic import op
import sqlalchemy as sa


revision = '0fe55be174c6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('vacancies_currency',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies_platform',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies_schedule',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies_town',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancies_vacancy',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('resource_id', sa.Integer(), nullable=True),
        sa.Column('platform_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('town_id', sa.Integer(), nullable=True),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('salary_from', sa.Integer(), nullable=True),
        sa.Column('salary_to', sa.Integer(), nullable=True),
        sa.Column('currency', sa.Integer(), nullable=True),
        sa.Column('gross', sa.Boolean(), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=True),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('requirement', sa.String(), nullable=False),
        sa.Column('responsibility', sa.String(), nullable=False),
        sa.Column('schedule', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['currency'], ['vacancies_currency.id'], ),
        sa.ForeignKeyConstraint(['platform_id'], ['vacancies_platform.id'], ),
        sa.ForeignKeyConstraint(['schedule'], ['vacancies_schedule.id'], ),
        sa.ForeignKeyConstraint(['town_id'], ['vacancies_town.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('vacancies_vacancy')
    op.drop_table('vacancies_town')
    op.drop_table('vacancies_schedule')
    op.drop_table('vacancies_platform')
    op.drop_table('vacancies_currency')
