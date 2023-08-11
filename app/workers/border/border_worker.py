import random
import time
from datetime import date, timedelta
from typing import Any, Dict, Optional
from urllib.parse import quote

import cloudscraper
from sqlalchemy.orm import Session

from app.db.engine_database import EngineDatabase
from app.models.common.date_range import DateRange
from app.models.common.response import Response
from app.models.common.result_status import ResultStatus
from app.models.domain.base import DataDB
from app.repos.data_repo import DataRepo
from app.workers.common.base_worker import BaseWorker
from app.workers.common.scrape_state import ScrapeState


class BorderWorker(BaseWorker[bool]):

    def __init__(self, border_url: str,
                 border: str,
                 cookie_url: str,
                 headers: Dict[str, Any],
                 date_range: DateRange,
                 data_repo: DataRepo,
                 engine: EngineDatabase) -> None:
        super().__init__()
        self._border_url = border_url
        self._border = border
        self._cookie_url = cookie_url
        self._headers = headers
        self._date_range = date_range

        self._data_repo = data_repo

        self._state = ScrapeState()
        self._engine = engine

    def result(self) -> bool:
        return not (self._is_abort() or self._is_cancel())

    @staticmethod
    def safe_request(client, url: str, params: Dict[str, str], headers: Dict[str, Any]) -> Response:
        try:
            response = client.post(quote(url, safe='/:&=?%#'), data=params, headers=headers)
            response.raise_for_status()
            return Response.success(data=response.json())
        except Exception as err:
            return Response.error(message=f"{type(err)} - {err}")

    def run(self):
        print(f"Thread is running...")
        completed = False
        with self._engine.get_session() as session:
            while self.is_running() and not completed:
                scraper = cloudscraper.create_scraper(delay=30, debug=False)
                scraper.get(self._cookie_url)
                for day in range(self._date_range.number_of_days()):
                    record_at = self._date_range.start_date + timedelta(days=day)
                    record = self.fetch_one_by(session, self._border, record_at)
                    if record is None or record.status != ResultStatus.success:
                        params = self._make_request_params(self._border, record_at)
                        result = self.safe_request(scraper, self._border_url, params, self._headers)
                        self._state.apply(result.status)
                        successfully = self._update(session, record.data_id, result) if record else self._insert(session, record_at, result)

                        if not successfully:
                            break  # self._state.fatal_error(result.status)

                        session.commit()
                        if self._is_abort() or completed or not self.is_running():
                            break

                        time.sleep(random.randint(1, 5))

                completed = True
                session.commit()

        print(f"Thread stopped. {self._state}")

    def _is_abort(self) -> bool:
        return self._state.abort(errors_greater=100, mse_greater=0.3)

    def _insert(self, session: Session, record_at: date, result: Response[Dict[str, Any]]) -> bool:
        try:
            self._data_repo.insert(session, record_at, self._border, result)
        except Exception as e:
            print(f"{type(e)}, message = {e}")
            return False
        return True

    def _update(self, session: Session, data_id: int, result: Response[Dict[str, Any]]) -> bool:
        try:
            self._data_repo.update(session, data_id, result)
        except Exception as e:
            print(f"{type(e)}, message = {e}")
            return False
        return True

    def fetch_one_by(self, session: Session, border: str, record_at: date) -> Optional[DataDB]:
        return self._data_repo.fetch_one_by(session, border=border, record_at=record_at)

    @staticmethod
    def _make_request_params(border: str, record_at: date) -> Dict[str, str]:
        return {"ppr": border, "date": record_at.strftime("%d.%m.%Y")}
