"""empty message

Revision ID: a20ece613f3b
Revises: 0f68ee24ff10
Create Date: 2024-06-14 21:06:19.483424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a20ece613f3b'
down_revision = '0f68ee24ff10'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message_to_excercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('excercise_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['excercise_id'], ['excercise.id'], ),
    sa.ForeignKeyConstraint(['message_id'], ['message.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('message_to_excercise', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_message_to_excercise_excercise_id'), ['excercise_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_message_to_excercise_message_id'), ['message_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message_to_excercise', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_message_to_excercise_message_id'))
        batch_op.drop_index(batch_op.f('ix_message_to_excercise_excercise_id'))

    op.drop_table('message_to_excercise')
    # ### end Alembic commands ###
