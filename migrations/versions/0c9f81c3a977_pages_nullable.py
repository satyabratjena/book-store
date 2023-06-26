"""pages nullable

Revision ID: 0c9f81c3a977
Revises: 06a78c7734f5
Create Date: 2023-06-21 03:00:15.512746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c9f81c3a977'
down_revision = '06a78c7734f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('pages',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.alter_column('pages',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###