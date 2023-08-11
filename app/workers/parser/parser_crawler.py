from injector import inject

from app.workers.common.base_crawler import BaseCrawler
from app.workers.parser.parser_worker_factory import ParserWorkerFactory


class ParserCrawler(BaseCrawler[bool]):
    @inject
    def __init__(self, worker_factory: ParserWorkerFactory):
        super().__init__()
        self._worker_factory = worker_factory
        self._worker = None

    def scrape(self) -> bool:
        self._worker = self._worker_factory.of()

        self._worker.start()
        self._wait()

        return True

    def stop(self):
        if self._worker:
            self._worker.stop()
            self._wait()

    def _wait(self):
        self._worker.join()
