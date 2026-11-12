from alembic import op
import sqlalchemy as sa
revision = "002_source"
down_revision = "001_initial"
branch_labels = None
depends_on = None

def upgrade() -> None:
    # TODO M06: source 열을 추가하세요.
    # TODO M07: source 인덱스를 추가하세요.
    raise NotImplementedError("TODO M06/M07")

def downgrade() -> None:
    # TODO M08: 인덱스와 열을 역순으로 제거하세요.
    raise NotImplementedError("TODO M08")
