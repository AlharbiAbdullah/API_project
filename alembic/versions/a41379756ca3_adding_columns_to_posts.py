"""adding columns to posts

Revision ID: a41379756ca3
Revises: 81ba4e20e8b6
Create Date: 2022-12-07 19:46:58.854484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a41379756ca3'
down_revision = '81ba4e20e8b6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts' , 
    sa.Column('content', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('posts' , 'content')
