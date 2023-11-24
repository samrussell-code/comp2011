"""hm

Revision ID: 169bb2e0af7f
Revises: 
Create Date: 2023-11-18 13:43:57.015852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '169bb2e0af7f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_like', schema=None) as batch_op:
        batch_op.add_column(sa.Column('test', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_like', schema=None) as batch_op:
        batch_op.drop_column('test')

    # ### end Alembic commands ###
