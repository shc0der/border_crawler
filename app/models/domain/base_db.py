import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class BaseDB(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
