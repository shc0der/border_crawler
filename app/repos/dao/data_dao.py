from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.common.response import Response
from app.models.domain.base import DataDB
from app.repos.dao.base_dao import BaseDao


class DataDao(BaseDao):
    def insert(self, session: Session, record_at: date, border: str, data: Response) -> DataDB:
        #update_data = self._obtain_update(data)
        return session.scalar(DataDB.insert(record_at=record_at,
                                            border=border,
                                            status=data.status,
                                            payload=data.model_dump()))

    def update(self, session: Session, data_id: int, data: Response) -> DataDB:
        return session.scalar(DataDB.update(data_id=data_id, status=data.status, payload=data.model_dump()))

    def fetch_all(self, session: Session) -> List[DataDB]:
        return session.scalars(DataDB.fetch_all()).all() or []

    def fetch_one_by(self, session: Session, border: str, record_at: date) -> Optional[DataDB]:
        return session.scalar(DataDB.fetch_one_by(border, record_at))
