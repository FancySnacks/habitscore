from __future__ import annotations

from datetime import date, datetime

from task import TaskPreset
from timeunit import Day, Year, Month, Week


def is_leap_year(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
    return False


def int_to_weekday(n: int) -> str:
    mapping = {1: 'Monday',
               2: 'Tuesday',
               3: 'Wednesday',
               4: 'Thursday',
               5: 'Friday',
               6: 'Saturday',
               7: 'Sunday',
               }

    return mapping[n]


def int_to_month(n: int) -> str:
    mapping = {1: 'January',
               2: 'February',
               3: 'March',
               4: 'April',
               5: 'May',
               6: 'June',
               7: 'July',
               8: 'August',
               9: 'September',
               10: 'October',
               11: 'November',
               12: 'December',
               }

    return mapping[n]


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
        # first load from save file, only then create dynamically
        # if load from save file: update all the way to current day

        c_month = 1
        c_week = 1
        c_day = 1
        day_of_the_week = 1

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


cal = Calendar()
cal.load_calendar()
