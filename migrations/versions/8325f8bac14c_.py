"""empty message

Revision ID: 8325f8bac14c
Revises: 3f5221b66e15
Create Date: 2017-06-09 00:49:27.275245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8325f8bac14c'
down_revision = '3f5221b66e15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decision', sa.Column('topic', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('decision', 'topic')
    # ### end Alembic commands ###