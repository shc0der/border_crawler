from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.db.engine_database import EngineDatabase
from app.models.common.result_status import ResultStatus
from app.models.domain.data_db import DataDB
from app.models.schema.border import BorderCreate
from app.repos.border_repo import BorderRepo
from app.repos.data_repo import DataRepo
from app.workers.common.base_worker import BaseWorker
from app.workers.common.scrape_state import ScrapeState


class ParserWorker(BaseWorker[bool]):

    def __init__(self,
                 data_repo: DataRepo,
                 border_repo: BorderRepo,
                 engine: EngineDatabase) -> None:
        super().__init__()
        self._data_repo = data_repo
        self._border_repo = border_repo

        self._state = ScrapeState()
        self._engine = engine

    def result(self) -> bool:
        return not (self._is_abort() or self._is_cancel())

    def run(self):
        print(f"Thread is running...")
        completed = False
        with self._engine.get_session() as session:
            while self.is_running() and not completed:
                for record in self._data_repo.fetch_all(session) or []:
                    items = self._items_parsing(record.border, self._get_response_items(record))
                    insert_status = self._insert(session, items)
                    self._state.apply(insert_status)
                    if not insert_status.is_success():
                        break

                completed = True

        print(f"Thread stopped. {self._state}")

    def _is_abort(self) -> bool:
        return self._state.abort(errors_greater=100, mse_greater=0.3)

    def _insert(self, session: Session, items: List[BorderCreate]) -> ResultStatus:
        try:
            if items:
                self._border_repo.insert_all(session, items)
                session.commit()
        except Exception as e:
            print(f"{type(e)}, message = {e}")
            return ResultStatus.error
        return ResultStatus.success

    @staticmethod
    def _get_response_items(record: DataDB) -> List[Dict[str, Any]]:
        if record.status == ResultStatus.success and record.payload.get("status") == ResultStatus.success:
            data = record.payload.get("data") or {}
            return data.get("ITEMS") or []
        return []

    @staticmethod
    def _items_parsing(border: str, items: List[Dict[str, Any]]) -> List[BorderCreate]:
        key_for_cars = f"PROPERTY_{border.upper()}_OUT_L_VALUE"
        records = []
        for index, row in enumerate(items):
            unsafe_datetime = row["NAME"].strip()
            try:
                safe_datetime = ParserWorker._convert_to_datetime(unsafe_datetime, index)
                records.append(BorderCreate(border=border,
                                            record_at=safe_datetime,
                                            cars=row[key_for_cars]))
            except ValueError:
                pass

        return records

    @staticmethod
    def _convert_to_datetime(unsafe_datetime: str, time_index: int) -> datetime:
        strip_datetime = unsafe_datetime.strip()
        size = len(strip_datetime)
        if size == 10:
            strip_datetime = "%s %02d:00:00" % (strip_datetime, time_index * 2)
        elif size == 16:
            strip_datetime += ":00"
        try:
            return datetime.strptime(strip_datetime, '%d.%m.%Y %H:%M:%S')
        except ValueError:
            strip_datetime = strip_datetime.replace(".00:00", ":00:00")
            return datetime.strptime(strip_datetime, '%d.%m.%Y %H:%M:%S')
