"""empty message

Revision ID: ea279dbf76ed
Revises: a18a3c0337a9
Create Date: 2020-09-07 19:27:15.790493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea279dbf76ed'
down_revision = 'a18a3c0337a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'category')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('category', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###