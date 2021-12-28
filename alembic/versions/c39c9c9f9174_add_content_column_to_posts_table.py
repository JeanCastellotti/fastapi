"""Add content column to posts table

Revision ID: c39c9c9f9174
Revises: 35b4a65d8664
Create Date: 2021-12-28 09:50:48.267017

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c39c9c9f9174'
down_revision = '35b4a65d8664'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.Text(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
