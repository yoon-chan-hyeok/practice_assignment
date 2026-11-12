from alembic import op
import sqlalchemy as sa
revision = "002_source"
down_revision = "001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # TODO M01: knowledge에 source VARCHAR(120) NULL 허용 열을 추가하세요.
    raise NotImplementedError("TODO M01")

def downgrade() -> None:
    # TODO M02: source 열을 제거하세요.
    raise NotImplementedError("TODO M02")
