"""create exchange_rate table

Revision ID: 4dcc07d00e28
Revises: 
Create Date: 2021-10-12 10:15:51.979381

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "4dcc07d00e28"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "exchange_rates",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("currency_from", sa.String(3), index=True),
        sa.Column("currency_to", sa.String(3), index=True),
        sa.Column("rate", sa.Numeric),
        sa.Column("ex_rt_date", sa.Date, index=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
    )


def downgrade():
    op.drop_table("exchange_date")
