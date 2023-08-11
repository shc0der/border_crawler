from datetime import date
from threading import Thread, Event
from typing import Optional, List

from injector import inject

from app.workers.border.border_crawler import BorderCrawler
from app.workers.parser.parser_crawler import ParserCrawler


class CrawlerPoolExecutor:
    @inject
    def __init__(self, border_crawler: BorderCrawler, parser_crawler: ParserCrawler) -> None:
        self._border_crawler = border_crawler
        self._parser_crawler = parser_crawler

        self._thread: Optional[Thread] = None
        self._is_running: Event = Event()

    def setup(self, borders: List[str], start_date: date, end_date: date):
        self._border_crawler.setup(borders, start_date, end_date)

    def run_in_background(self):
        print("aggregation process started")

        if self._border_crawler.scrape():
            self._parser_crawler.scrape()

        self._is_running.clear()
        self._thread = None

        print("the aggregation process is completed")

    def start(self):
        if self._thread is None or not self.is_running():
            self._thread = Thread(target=self.run_in_background)
            self._is_running.set()
            self._thread.start()
        else:
            print("Processing cannot be started. To start a new processing, stop the previous one")

    def is_running(self) -> bool:
        return self._is_running.is_set()

    def stop(self):
        print(f"stopping the thread and child workers")
        if self._thread and self.is_running():
            self._border_crawler.stop()

    def wait(self):
        if self._thread and self.is_running():
            self._thread.join()
