from abc import ABC, abstractmethod
from typing import TypeVar, Generic

ResultData = TypeVar('ResultData')


class BaseCrawler(ABC, Generic[ResultData]):

    @abstractmethod
    def scrape(self) -> ResultData:
        pass

    @abstractmethod
    def stop(self):
        pass
