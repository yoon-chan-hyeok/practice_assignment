from alembic import op
import sqlalchemy as sa
revision = "002_source"
down_revision = "001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column("knowledge", sa.Column("source", sa.String(120), nullable=True))

def downgrade() -> None:
    op.drop_column("knowledge", "source")
