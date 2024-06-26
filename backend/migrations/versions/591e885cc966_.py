"""empty message

Revision ID: 591e885cc966
Revises: 5f05da140ec9
Create Date: 2024-06-14 17:03:40.194413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '591e885cc966'
down_revision = '5f05da140ec9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('excercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=4096), nullable=True),
    sa.Column('muscles', postgresql.ARRAY(sa.String(length=80)), nullable=True),
    sa.Column('type', sa.String(length=80), nullable=True),
    sa.Column('equipment', postgresql.ARRAY(sa.String(length=80)), nullable=True),
    sa.Column('difficulty', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('excercise_to_image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('excercise_id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['excercise_id'], ['excercise.id'], ),
    sa.ForeignKeyConstraint(['image_id'], ['image.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('excercise_to_image', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_excercise_to_image_excercise_id'), ['excercise_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('excercise_to_image', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_excercise_to_image_excercise_id'))

    op.drop_table('excercise_to_image')
    op.drop_table('excercise')
    # ### end Alembic commands ###
