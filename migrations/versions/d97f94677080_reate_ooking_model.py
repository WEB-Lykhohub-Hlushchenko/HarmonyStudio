"""reate ooking model

Revision ID: d97f94677080
Revises: 54a3db853ddb
Create Date: 2024-11-25 21:51:14.823518

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd97f94677080'
down_revision = '54a3db853ddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('booking_datetime', sa.DateTime(), nullable=False))
        batch_op.alter_column('status',
               existing_type=mysql.VARCHAR(length=20),
               type_=sa.String(length=50),
               existing_nullable=False)
        batch_op.drop_column('time')
        batch_op.drop_column('date')

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_column('patronymic')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('middle_name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('middle_name', mysql.VARCHAR(length=50), nullable=True))

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('patronymic', mysql.VARCHAR(length=50), nullable=True))

    with op.batch_alter_table('booking', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date', sa.DATE(), nullable=False))
        batch_op.add_column(sa.Column('time', mysql.TIME(), nullable=False))
        batch_op.alter_column('status',
               existing_type=sa.String(length=50),
               type_=mysql.VARCHAR(length=20),
               existing_nullable=False)
        batch_op.drop_column('booking_datetime')

    # ### end Alembic commands ###
