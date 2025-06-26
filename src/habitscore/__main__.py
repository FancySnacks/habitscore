"""Main entry script"""

from __future__ import annotations

import json
import os

from datetime import date, datetime

from habitscore.util import is_leap_year, int_to_weekday
from habitscore.task import TaskPreset
from habitscore.timeunit import Day, Year, Month, Week
from habitscore.const import PRESET_SAVE_PATH


NOW = datetime.now()
CURRENT_YEAR: int = NOW.year

MONTHS = {'January': 31,
          'February': 29 if is_leap_year(CURRENT_YEAR) else 28,
          'March': 31,
          'April': 30,
          'May': 31,
          'June': 30,
          'July': 31,
          'August': 31,
          'September': 30,
          'October': 31,
          'November': 30,
          'December': 31}


class Calendar:
    def __init__(self):
        self.today: Day
        self.years: list[Year] = []

    def load_calendar(self):
        if self.year_save_exists(NOW.year):
            self.import_year_from_file()
            return

        c_month = 1
        c_week = 1
        c_day = 1

        months: list[Month] = []
        weeks: list[Week] = []
        days: list[Day] = []

        # Loop through months
        for item in MONTHS.items():
            month_daycount = item[1]
            day_of_the_week = 1

            # Create Day object for every day in a given month
            for day_i in range(1, month_daycount + 1):
                day_date = date(date.today().year, c_month, day_i)
                weekday = day_date.isoweekday()

                day = Day(name=int_to_weekday(weekday),
                          weekly_index=day_of_the_week,
                          monthly_index=day_i,
                          yearly_index=c_day,
                          tasks=TaskPreset("Default Preset", [])
                          )

                days.append(day)

                c_day += 1
                day_of_the_week += 1

                # Create Week object
                if weekday == 7:
                    week = Week(c_week, days[:])
                    weeks.append(week)
                    days.clear()
                    day_of_the_week = 1
                    c_week += 1

            # Create Month object
            month = Month(item[0], c_month, weeks[:])
            months.append(month)
            weeks.clear()

            c_month += 1

        # Create Year object
        year = Year(CURRENT_YEAR, months)
        self.years.append(year)

        self.today = self.get_today()

        # load each day preset

    def get_today(self) -> Day:
        return self.years[-1].months[NOW.month - 1].days[NOW.day - 1]

    def get_current_year(self) -> Year:
        return self.years[-1]

    def import_year_from_file(self):
        with open(PRESET_SAVE_PATH.joinpath(f"{NOW.year}.json"), 'r') as file:
            json_data = json.load(file)
            year = Year.year_from_file(json_data)

            self.years.append(year)
            self.today = self.get_today()

    def year_save_exists(self, year: int) -> bool:
        return os.path.exists(PRESET_SAVE_PATH.joinpath(f"{year}.json"))

    def save_year_to_file(self):
        current_year = self.get_current_year()

        with open(PRESET_SAVE_PATH.joinpath(f"{current_year.year}.json"), "w+") as file:
            json_data = current_year.to_json()
            json.dump(json_data, file, indent=5)


def main() -> int:
    cal = Calendar()
    cal.load_calendar()
    cal.save_year_to_file()
    cal.today.print()

    return 0


if __name__ == '__main__':
    SystemExit(main())
