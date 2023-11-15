"""empty message

Revision ID: 550ee7b8f660
Revises: 0e58a087018d
Create Date: 2023-11-14 13:54:49.534878

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '550ee7b8f660'
down_revision = '0e58a087018d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_selected', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profile', schema=None) as batch_op:
        batch_op.drop_column('is_selected')

    # ### end Alembic commands ###