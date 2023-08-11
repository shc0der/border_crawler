from datetime import date

from sqlalchemy import String, Integer, Date, select, and_, update
from sqlalchemy.dialects.postgresql import JSONB, insert
from sqlalchemy.orm import Mapped, mapped_column

from app.models.common.result_status import ResultStatus
from app.models.domain.base import BaseDB


class DataDB(BaseDB):
    data_id: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, index=True, autoincrement=True)
    record_at: Mapped[date] = mapped_column(Date(), index=True)
    border: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[ResultStatus] = mapped_column(String, default=ResultStatus.error)
    payload: Mapped[dict] = mapped_column(JSONB, default={})

    @staticmethod
    def insert(**kwargs) -> insert:
        return insert(DataDB).values(kwargs).returning(DataDB)

    @staticmethod
    def update(data_id: int, **kwargs) -> insert:
        return update(DataDB).where(DataDB.data_id == data_id).values(kwargs).returning(DataDB)

    # @staticmethod
    # def insert(**kwargs) -> insert:
    #     return insert(DataDB)\
    #         .values(**kwargs)\
    #         .on_conflict_do_update(index_elements=[DataDB.data_id],
    #                                set_={"payload": {}})\
    #         .returning(DataDB)

    @staticmethod
    def fetch_all() -> select:
        return select(DataDB)

    @staticmethod
    def fetch_one_by(border: str, record_at: date) -> select:
        return select(DataDB).where(and_(DataDB.border == border,
                                         DataDB.record_at == record_at))
