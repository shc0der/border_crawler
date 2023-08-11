from enum import Enum


class ResultStatus(str, Enum):
    success = "success"
    error = "error"

    def is_success(self) -> bool:
        return self == ResultStatus.success
