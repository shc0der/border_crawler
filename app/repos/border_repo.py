from typing import List

from injector import inject
from sqlalchemy.orm import Session

from app.models.domain.base import BorderDB
from app.models.schema.border import BorderCreate
from app.repos.base_repo import BaseRepo
from app.repos.dao.border_dao import BorderDao


class BorderRepo(BaseRepo):
    @inject
    def __init__(self, border_dao: BorderDao) -> None:
        self._border_dao = border_dao

    def insert(self, session: Session, body: BorderCreate) -> BorderDB:
        return self._border_dao.insert(session, **body.model_dump())

    def insert_all(self, session: Session, items: List[BorderCreate]) -> List[BorderDB]:
        return self._border_dao.insert_all(session, items)
