"""updated invioce

Revision ID: 59f3632bf017
Revises: 6a37c17415c5
Create Date: 2024-05-19 09:48:07.385863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59f3632bf017'
down_revision = '6a37c17415c5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'customer_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('invoices', 'customer_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###
