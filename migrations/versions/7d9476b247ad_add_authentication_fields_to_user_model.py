"""Add authentication fields to User model

Revision ID: 7d9476b247ad
Revises: e255840f62ad
Create Date: 2024-11-23 18:57:32.102898

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7d9476b247ad'
down_revision = 'e255840f62ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('middle_name', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('date_of_birth', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=15), nullable=False))
        batch_op.add_column(sa.Column('password_hash', sa.String(length=200), nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', mysql.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('password_hash')
        batch_op.drop_column('phone_number')
        batch_op.drop_column('date_of_birth')
        batch_op.drop_column('middle_name')

    # ### end Alembic commands ###