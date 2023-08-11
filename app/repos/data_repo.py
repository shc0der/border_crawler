from datetime import date
from typing import List, Optional

from injector import inject
from sqlalchemy.orm import Session

from app.models.common.response import Response
from app.models.domain.base import DataDB
from app.repos.base_repo import BaseRepo
from app.repos.dao.data_dao import DataDao


class DataRepo(BaseRepo):

    @inject
    def __init__(self, data_dao: DataDao) -> None:
        self._data_dao = data_dao

    def insert(self, session: Session, record_at: date, border: str, data: Response) -> DataDB:
        return self._data_dao.insert(session, record_at, border, data)

    def update(self, session: Session, data_id: int, data: Response) -> DataDB:
        return self._data_dao.update(session, data_id, data)

    def fetch_all(self, session: Session) -> List[DataDB]:
        return self._data_dao.fetch_all(session)

    def fetch_one_by(self, session: Session, border: str, record_at: date) -> Optional[DataDB]:
        return self._data_dao.fetch_one_by(session, border, record_at)
