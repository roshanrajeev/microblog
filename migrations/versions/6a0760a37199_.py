"""empty message

Revision ID: 6a0760a37199
Revises: f1b6488d0eae
Create Date: 2020-12-14 23:35:41.152045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a0760a37199'
down_revision = 'f1b6488d0eae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('recipient_id', sa.Integer(), nullable=False))
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['recipient_id'], ['id'])
    op.drop_column('message', 'receiver_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('receiver_id', sa.INTEGER(), nullable=False))
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['receiver_id'], ['id'])
    op.drop_column('message', 'recipient_id')
    # ### end Alembic commands ###
