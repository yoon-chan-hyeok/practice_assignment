from alembic import op
import sqlalchemy as sa
revision = "002_source"
down_revision = "001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # TODO M03: source 열을 추가하세요.
    # TODO M04: source 조회용 인덱스를 추가하세요.
    raise NotImplementedError("TODO M03/M04")

def downgrade() -> None:
    # TODO M05: 인덱스와 열을 안전한 역순으로 제거하세요.
    raise NotImplementedError("TODO M05")
