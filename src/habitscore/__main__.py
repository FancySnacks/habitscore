from __future__ import annotations

import json
import datetime

from task import TaskPreset
from timeunit import Day, Year, Month, Week

presets: dict[str: dict] = {}
days_o: list[Day] = []


def load_presets():
    # for file in habit preset folder, load file
    # add to global presets list

    with open("../../data/presets/habits/habits_preset_1.json", "r") as file:
        data = json.load(file)
        preset = TaskPreset(**data)
        presets[preset.name] = preset


def load_weekdays_preset():
    with open("../../data/presets/weekdays_preset.json", "r") as file:
        days: list[dict] = json.load(file)['weekdays']

        for day in days:
            habit_preset = presets.get(day['preset_name'])
            new_day = Day(name=day['name'], tasks=habit_preset)
            days_o.append(new_day)


load_presets()
load_weekdays_preset()

now = datetime.datetime.now()
current_day = days_o[now.day % len(days_o)]
current_week = Week([current_day])

# create days based on month day count

# create weeks dynamically in segments of 1-7 days
# then assign weeks to months

months: list[Month] = []

for c in range(1, 13):
    new_month = Month(c, [current_week])
    months.append(new_month)

current_year: int = now.year
year = Year(current_year, months)


class Calendar:
    def __init__(self):
        self.years: list[Year] = []
        self.current_year: Year

    def load_calendar(self):
        # first load from save file
        now = datetime.datetime.now()
        current_year: int = now.year
        year_o = Year(current_year, months)

        # create a year
        # create all 12 months
        # populate each week with days
        # load each day preset
