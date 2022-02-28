"""empty message

Revision ID: 0feb465a1a84
Revises: 9caba2f6ff77
Create Date: 2022-02-28 17:03:06.509588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0feb465a1a84'
down_revision = '9caba2f6ff77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('customer', 'opt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('opt', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
