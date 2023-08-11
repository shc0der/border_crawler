from datetime import date
from typing import List

from injector import inject

from app.models.common.date_range import DateRange
from app.workers.border.border_worker_factory import BorderWorkerFactory
from app.workers.common.base_crawler import BaseCrawler


class BorderCrawler(BaseCrawler[bool]):
    @inject
    def __init__(self, worker_factory: BorderWorkerFactory):
        super().__init__()
        self._borders = []
        self._date_range = None
        self._worker_factory = worker_factory
        self._workers = None

    def setup(self, borders: List[str], start_date: date, end_date: date):
        self._borders = borders
        self._date_range = DateRange(start_date=start_date, end_date=end_date)

    def scrape(self) -> bool:
        self._workers = [self._worker_factory.of(border, self._date_range) for border in self._borders]
        for worker in self._workers:
            worker.start()

        self._wait()

        return True

    def stop(self):
        if self._workers:
            for worker in self._workers:
                worker.stop()

            self._wait()

    def _wait(self):
        for worker in self._workers:
            worker.join()
