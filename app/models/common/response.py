from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

from app.models.common.result_status import ResultStatus

Data = TypeVar("Data")


class Response(BaseModel, Generic[Data]):
    data: Optional[Data] = None
    message: Optional[str] = None
    status: ResultStatus = ResultStatus.success

    @staticmethod
    def error(message: Optional[str]):
        return Response(message=message, status=ResultStatus.error)

    @staticmethod
    def success(data: Optional[Data]):
        return Response(data=data, status=ResultStatus.success)
