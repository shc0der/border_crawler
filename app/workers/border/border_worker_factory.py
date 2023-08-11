from typing import Dict, Any

from app.db.engine_database import EngineDatabase
from app.models.common.date_range import DateRange
from app.repos.data_repo import DataRepo
from app.workers.border.border_worker import BorderWorker


class BorderWorkerFactory:
    def __init__(self, border_url: str, cookie_url: str, headers: Dict[str, Any], data_repo: DataRepo, engine: EngineDatabase) -> None:
        super().__init__()
        self._border_url = border_url
        self._cookie_url = cookie_url
        self._headers = headers
        self._data_repo = data_repo
        self._engine = engine

    def of(self, border: str, date_range: DateRange) -> BorderWorker:
        return BorderWorker(self._border_url,
                            border,
                            self._cookie_url,
                            self._headers,
                            date_range,
                            self._data_repo,
                            self._engine)
