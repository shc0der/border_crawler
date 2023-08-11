from app.db.engine_database import EngineDatabase
from app.repos.border_repo import BorderRepo
from app.repos.data_repo import DataRepo
from app.workers.parser.parser_worker import ParserWorker


class ParserWorkerFactory:
    def __init__(self, data_repo: DataRepo, border_repo: BorderRepo, engine: EngineDatabase) -> None:
        super().__init__()
        self._data_repo = data_repo
        self._border_repo = border_repo
        self._engine = engine

    def of(self) -> ParserWorker:
        return ParserWorker(self._data_repo,
                            self._border_repo,
                            self._engine)
