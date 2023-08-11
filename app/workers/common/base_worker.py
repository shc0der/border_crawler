from abc import abstractmethod
from typing import TypeVar, Generic

from app.workers.common.worker_thread import WorkerThread


ResultData = TypeVar('ResultData')


class BaseWorker(WorkerThread, Generic[ResultData]):

    @abstractmethod
    def result(self) -> ResultData:
        pass
