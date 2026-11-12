from sqlalchemy import BigInteger, CheckConstraint, ForeignKey, Identity, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# PostgreSQL에서는 BIGINT, SQLite 기반 정적 검수에서는 INTEGER가 되도록 정의합니다.
ID_TYPE = Integer().with_variant(BigInteger, "postgresql")

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint("char_length(name) BETWEEN 1 AND 30", name="categories_name_length"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    knowledge_items: Mapped[list["Knowledge"]] = relationship(back_populates="category")

class Knowledge(Base):
    __tablename__ = "knowledge"
    __table_args__ = (
        CheckConstraint("char_length(title) BETWEEN 1 AND 80", name="knowledge_title_length"),
        CheckConstraint("char_length(content) BETWEEN 1 AND 2000", name="knowledge_content_length"),
    )
    id: Mapped[int] = mapped_column(ID_TYPE, Identity(always=True), primary_key=True)
    title: Mapped[str] = mapped_column(String(80), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(
        ID_TYPE, ForeignKey("categories.id", ondelete="RESTRICT", name="knowledge_category_fk"), nullable=False
    )
    category: Mapped[Category] = relationship(back_populates="knowledge_items")
