"""empty message

Revision ID: 0f68ee24ff10
Revises: 591e885cc966
Create Date: 2024-06-14 18:04:10.803637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f68ee24ff10'
down_revision = '591e885cc966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('excercise', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=4096),
               nullable=False)
        batch_op.create_unique_constraint(None, ['name'])

    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['filename'])

    with op.batch_alter_table('trainer_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('experience', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trainer_profile', schema=None) as batch_op:
        batch_op.drop_column('experience')

    with op.batch_alter_table('image', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    with op.batch_alter_table('excercise', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=4096),
               nullable=True)

    # ### end Alembic commands ###
