from datetime import datetime

from pydantic import BaseModel


class BorderCreate(BaseModel):
    record_at: datetime
    border: str
    cars: int
