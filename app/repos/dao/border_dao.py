from typing import List

from sqlalchemy.orm import Session

from app.models.domain.base import BorderDB
from app.models.schema.border import BorderCreate
from app.repos.dao.base_dao import BaseDao


class BorderDao(BaseDao):

    def insert(self, session: Session, body: BorderCreate) -> BorderDB:
        return session.scalar(BorderDB.insert(**body.model_dump()))

    def insert_all(self, session: Session, items: List[BorderCreate]) -> List[BorderDB]:
        return session.scalars(BorderDB.insert_all([item.model_dump() for item in items])).all() or []
