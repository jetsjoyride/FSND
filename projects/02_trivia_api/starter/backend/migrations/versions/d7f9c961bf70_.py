"""empty message

Revision ID: d7f9c961bf70
Revises: 
Create Date: 2020-09-07 15:41:27.492571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7f9c961bf70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('categories', 'type',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('questions', 'answer',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.alter_column('questions', 'question',
               existing_type=sa.TEXT(),
               type_=sa.String(),
               existing_nullable=True)
    op.drop_constraint('category', 'questions', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('category', 'questions', 'categories', ['category'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    op.alter_column('questions', 'question',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('questions', 'answer',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    op.alter_column('categories', 'type',
               existing_type=sa.String(),
               type_=sa.TEXT(),
               existing_nullable=True)
    # ### end Alembic commands ###
