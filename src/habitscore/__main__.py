from __future__ import annotations

from datetime import date, datetime

from task import TaskPreset
from timeunit import Day, Year, Month, Week


class Calendar:
    def __init__(self):
        self.years: list[Year] = []
        self.current_year: Year

    def load_calendar(self):
        # first load from save file
        now = datetime.now()
        current_year: int = now.year

        mc = {'January': 31,
              'February': 29 if self.is_leap_year(current_year) else 28,
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

        year_day_count = sum(mc.values())
        year_week_count = year_day_count // 7

        c_month = 1
        c_week = 1
        day_of_the_week = 1

        weeks: list[Week] = []
        days: list[Day] = []

        for i in range(1, year_day_count + 1):
            day_date = date(date.today().year, c_month, i)
            weekday = day_date.isoweekday()
            monthday = i % mc.get(self.int_to_month(day_date.month))

            day = Day(name=self.int_to_weekday(weekday),
                      weekly_index=day_of_the_week,
                      monthly_index=monthday,
                      yearly_index=i,
                      tasks=TaskPreset("Default Preset", [])
                      )

            days.append(day)

            day_of_the_week += 1

            if day_of_the_week == 8:
                week = Week(c_week, days)
                weeks.append(week)
                days.clear()
                day_of_the_week = 1

        #days = [Day()]

        print(year_day_count)
        print(year_week_count)

        # create a year
        # create all 12 months
        # create weeks dynamically in segments of 1-7 days
        # then assign weeks to months
        # load each day preset

    def is_leap_year(self, year: int) -> bool:
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
        return False

    def int_to_weekday(self, n: int) -> str:
        mapping = {1: 'Monday',
                   2: 'Tuesday',
                   3: 'Wednesday',
                   4: 'Thursday',
                   5: 'Friday',
                   6: 'Saturday',
                   7: 'Sunday',
                   }

        return mapping[n]

    def int_to_month(self, n: int) -> str:
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


cal = Calendar()
cal.load_calendar()
