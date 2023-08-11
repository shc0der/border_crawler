from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def number_of_days(self) -> int:
        return (self.end_date - self.start_date).days
