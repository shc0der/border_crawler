from threading import Thread, Event
from typing import Callable, Any, Optional


class WorkerThread(Thread):

    def __init__(self, target: Optional[Callable[..., Any]] = ...) -> None:
        super().__init__(target=target)
        self._is_running = Event()
        self._is_cancel = Event()

    def is_running(self) -> bool:
        return self._is_running.is_set()

    def is_cancel(self) -> bool:
        return self._is_cancel.is_set()

    def start(self):
        self._is_running.set()
        super().start()

    def stop(self):
        self._is_cancel.set()
        self._is_running.clear()
