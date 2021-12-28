"""Create posts table

Revision ID: 35b4a65d8664
Revises: 
Create Date: 2021-12-27 22:05:23.475802

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '35b4a65d8664'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts', sa.Column('id',
                           sa.Integer(),
                           nullable=False,
                           primary_key=True),
        sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
