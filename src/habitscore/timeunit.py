from __future__ import annotations

import json
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from src.habitscore.util import weekday_to_int
from src.habitscore.task import TaskPreset


class TimeUnit(ABC):
    @abstractmethod
    def get_potential_score(self) -> int:
        pass

    @abstractmethod
    def get_total_score(self) -> int:
        pass

    def print(self):
        print(f"{self.get_total_score()}/{self.get_potential_score()}")


@dataclass(order=True)
class Day(TimeUnit):
    _sort_index: int = field(init=False, repr=False)
    name: str
    weekly_index: int
    monthly_index: int
    yearly_index: int
    tasks: TaskPreset

    def __post_init__(self):
        self._sort_index = self.monthly_index

    @classmethod
    def day_from_file(cls, json_data: dict) -> Day:
        with open(f"../../data/presets/weekdays_preset.json", 'r') as file:
            index = weekday_to_int(json_data['name']) - 1
            weekday = json.load(file)['weekdays'][index]
            preset_name = weekday['preset_name']

        preset_path = f"../../data/presets/tasks/{preset_name}.json"

        task_preset = TaskPreset.preset_from_file(preset_path)
        json_data.pop('preset_name')

        return Day(**json_data, tasks=task_preset)

    def get_potential_score(self) -> int:
        return sum(task.score for task in self.tasks.tasks)

    def get_total_score(self) -> int:
        return sum(task.score for task in self.tasks.tasks if task.is_completed)

    def to_json(self) -> dict:
        return {"name": self.name,
                "weekly_index": self.weekly_index,
                "monthly_index": self.monthly_index,
                "yearly_index": self.yearly_index,
                "preset_name": self.tasks.name}

    def print_tasks(self):
        return [print(task) for task in self.tasks.tasks]


@dataclass(order=True)
class Week(TimeUnit):
    _sort_index: int = field(init=False, repr=False)
    index: int
    days: list[Day]

    def __post_init__(self):
        self._sort_index = self.index

    @classmethod
    def week_from_file(cls, json_data: dict) -> Week:
        days = [Day.day_from_file(data) for data in json_data['days']]
        return Week(json_data['index'], days)

    def get_potential_score(self) -> int:
        return sum(day.get_potential_score() for day in self.days)

    def get_total_score(self) -> int:
        return sum(day.get_total_score() for day in self.days)

    def to_json(self) -> dict:
        return {"index": self.index,
                "days": [day.to_json() for day in self.days]}


@dataclass(order=True)
class Month(TimeUnit):
    _sort_index: int = field(init=False, repr=False)
    name: str
    index: int
    weeks: list[Week]
    days: list[Day] = field(init=False, default_factory=list)

    def __post_init__(self):
        self._sort_index = self.index

        days = [week.days for week in self.weeks]
        days_combined = []
        [days_combined.extend(d) for d in days]
        self.days = sorted(days_combined)

    @classmethod
    def month_from_file(cls, json_data: dict) -> Month:
        weeks = [Week.week_from_file(data) for data in json_data['weeks']]
        json_data.pop('weeks')
        return Month(**json_data, weeks=weeks)

    def get_potential_score(self) -> int:
        return sum(week.get_potential_score() for week in self.weeks)

    def get_total_score(self) -> int:
        return sum(week.get_total_score() for week in self.weeks)

    def to_json(self) -> dict:
        return {"name": self.name,
                "index": self.index,
                "weeks": [week.to_json() for week in self.weeks]}


@dataclass(order=True)
class Year(TimeUnit):
    _sort_index: int = field(init=False, repr=False)
    year: int
    months: list[Month]

    def __post_init__(self):
        self._sort_index = self.year

    @classmethod
    def year_from_file(cls, json_data: dict) -> Year:
        months = [Month.month_from_file(data) for data in json_data['months']]
        json_data.pop('months')
        return Year(json_data['year'], months=months)

    def get_potential_score(self) -> int:
        return sum(month.get_potential_score() for month in self.months)

    def get_total_score(self) -> int:
        return sum(month.get_total_score() for month in self.months)

    def s_today(self) -> str:
        return f"{len(self.months[-1].weeks[-1].days)} {self.months[-1]} {self.year}"

    def to_json(self) -> dict:
        return {"year": self.year,
                "months": [month.to_json() for month in self.months]}
