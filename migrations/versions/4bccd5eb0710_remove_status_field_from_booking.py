"""Remove status field from Booking

Revision ID: 4bccd5eb0710
Revises: 8d405a24c30b
Create Date: 2024-12-15 18:04:27.363975

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4bccd5eb0710'
down_revision = '8d405a24c30b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', mysql.VARCHAR(length=50), nullable=False))

    # ### end Alembic commands ###