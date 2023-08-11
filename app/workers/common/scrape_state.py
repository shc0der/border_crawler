from app.models.common.result_status import ResultStatus


class ScrapeState:

    def __init__(self, success: int = 0, errors: int = 0) -> None:
        super().__init__()
        self._success = success
        self._errors = errors

    def apply(self, status: ResultStatus):
        if status.is_success():
            self._success += 1
        else:
            self._errors += 1

    def abort(self, errors_greater: int, mse_greater: float) -> bool:
        mse = self._errors / (self._success or 1)
        return self._errors > errors_greater and mse >= mse_greater

    def total_number_of_requests(self) -> int:
        return self._success + self._errors

    def __repr__(self):
        return f"{self.__class__.__name__}: {vars(self)}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - number_of_success: {self._success}, number_of_errors: {self._errors}"


