"""adding post table

Revision ID: 81ba4e20e8b6
Revises: 
Create Date: 2022-12-07 19:33:38.009244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81ba4e20e8b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id' , 
    sa.Integer(), nullable= False, primary_key=True),
    sa.Column('title', sa.String()))

def downgrade() -> None:
    op.drop_table('posts')
