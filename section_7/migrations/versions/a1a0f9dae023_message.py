"""message

Revision ID: a1a0f9dae023
Revises: 6578edc7bb14
Create Date: 2023-11-08 10:10:55.136031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1a0f9dae023'
down_revision = '6578edc7bb14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('landlord',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=True),
    sa.Column('contact_number', sa.String(length=20), nullable=True),
    sa.Column('address', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('landlord', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_landlord_address'), ['address'], unique=True)
        batch_op.create_index(batch_op.f('ix_landlord_name'), ['name'], unique=False)

    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.add_column(sa.Column('landlord_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_landlord_id', 'landlord', ['landlord_id'], ['id'])
        batch_op.drop_column('owner')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owner', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint('fk_landlord_id', type_='foreignkey')
        batch_op.drop_column('landlord_id')

    with op.batch_alter_table('landlord', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_landlord_name'))
        batch_op.drop_index(batch_op.f('ix_landlord_address'))

    op.drop_table('landlord')
    # ### end Alembic commands ###
