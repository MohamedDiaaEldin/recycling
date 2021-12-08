"""empty message

Revision ID: 1989b6ac19a6
Revises: 
Create Date: 2021-12-08 06:10:08.375345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1989b6ac19a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employee')
    op.drop_table('department')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('department',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('department_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='department_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('employee',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('department_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], name='employee_department_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='employee_pkey')
    )
    # ### end Alembic commands ###
