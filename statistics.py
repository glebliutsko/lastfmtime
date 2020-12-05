import datetime


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
