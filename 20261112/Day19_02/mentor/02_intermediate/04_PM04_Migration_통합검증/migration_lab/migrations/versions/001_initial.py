from alembic import op
import sqlalchemy as sa
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("categories",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("name", sa.String(30), nullable=False),
        sa.CheckConstraint("char_length(name) BETWEEN 1 AND 30", name="categories_name_length"),
        sa.UniqueConstraint("name", name="categories_name_key"),
    )
    op.create_table("knowledge",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), primary_key=True),
        sa.Column("title", sa.String(80), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("category_id", sa.BigInteger(), nullable=False),
        sa.CheckConstraint("char_length(title) BETWEEN 1 AND 80", name="knowledge_title_length"),
        sa.CheckConstraint("char_length(content) BETWEEN 1 AND 2000", name="knowledge_content_length"),
        sa.ForeignKeyConstraint(["category_id"],["categories.id"],name="knowledge_category_fk",ondelete="RESTRICT"),
    )

def downgrade() -> None:
    op.drop_table("knowledge")
    op.drop_table("categories")
