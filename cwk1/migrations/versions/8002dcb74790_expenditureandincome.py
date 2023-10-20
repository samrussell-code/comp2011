"""expenditureandincome

Revision ID: 8002dcb74790
Revises: b07b84f3d56e
Create Date: 2023-10-20 23:46:05.353926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8002dcb74790'
down_revision = 'b07b84f3d56e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('income',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_income_name'), ['name'], unique=True)

    with op.batch_alter_table('expenditure', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', sa.Float(), nullable=True))
        batch_op.drop_index('ix_expenditure_name')
        batch_op.create_index(batch_op.f('ix_expenditure_name'), ['name'], unique=True)
        batch_op.drop_column('date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('expenditure', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DATETIME(), nullable=True))
        batch_op.drop_index(batch_op.f('ix_expenditure_name'))
        batch_op.create_index('ix_expenditure_name', ['name'], unique=False)
        batch_op.drop_column('amount')

    with op.batch_alter_table('income', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_income_name'))

    op.drop_table('income')
    # ### end Alembic commands ###
