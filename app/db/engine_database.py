from contextlib import contextmanager
from typing import Generator

from injector import inject
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class EngineDatabase:
    @inject
    def __init__(self, database_uri: str):
        self._engine = create_engine(database_uri, echo=True)
        self._session = sessionmaker(self._engine, expire_on_commit=False)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        with self._session() as session:
            yield session
