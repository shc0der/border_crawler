from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Mapped, mapped_column

from app.models.domain.base import BaseDB


class BorderDB(BaseDB):
    border_id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    record_at: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    border: Mapped[str] = mapped_column(String)
    cars: Mapped[str] = mapped_column(Integer)

    @staticmethod
    def insert(**kwargs) -> insert:
        return insert(BorderDB).values(kwargs).returning(BorderDB)

    @staticmethod
    def insert_all(items: List[Dict[str, Any]]) -> insert:
        return insert(BorderDB).values(items).returning(BorderDB)
