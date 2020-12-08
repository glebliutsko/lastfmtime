import datetime
from typing import Tuple, Generator, TextIO


class CsvOutput:
    def __init__(self, delimiter=';'):
        self._data = []
        self.delimiter = delimiter

    def add(self, *args: str):
        self._data.append(list(args))

    def __str__(self):
        lines = []
        for i in self._data:
            lines.append(self.delimiter.join(i))
        return '\n'.join(lines)

    def to_file(self, file: TextIO):
        file.write(str(self))


class Statistics:
    def __init__(self):
        self._days = {}

    def add_listening(self, date: datetime.date, seconds: int):
        iso = date.isoformat()
        if iso not in self._days:
            self._days[iso] = 0

        self._days[iso] += seconds

    def get_statistic_by_day(self) -> dict:
        return self._days.copy()

    def get_time_listening(self) -> int:
        all_seconds = 0
        for date_iso, seconds in self._days.items():
            all_seconds += seconds

        return all_seconds

    def export2csvfile(self, filename: str):
        csv = CsvOutput()
        for day, count_house in self:
            csv.add(day.isoformat(), str(count_house))

        with open(filename, 'w') as f:
            csv.to_file(f)

    def __iter__(self) -> Generator[Tuple[datetime.date, int], None, None]:
        for date, count_seconds in self._days.items():
            yield datetime.date.fromisoformat(date), count_seconds
