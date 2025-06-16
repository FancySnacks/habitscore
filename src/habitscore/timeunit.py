from __future__ import annotations

from dataclasses import dataclass, field
from abc import ABC, abstractmethod

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

    def get_potential_score(self) -> int:
        return sum(task.score for task in self.tasks.tasks)

    def get_total_score(self) -> int:
        return sum(task.score for task in self.tasks.tasks if task.is_completed)

    def __repr__(self) -> str:
        return f"{self.name} {self.monthly_index}, weekly = {self.weekly_index}, yearly = {self.yearly_index}"


@dataclass(order=True)
class Week(TimeUnit):
    _sort_index: int = field(init=False, repr=False)
    index: int
    days: list[Day]

    def __post_init__(self):
        self._sort_index = self.index

    def get_potential_score(self) -> int:
        return sum(day.get_potential_score() for day in self.days)

    def get_total_score(self) -> int:
        return sum(day.get_total_score() for day in self.days)


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


    def get_potential_score(self) -> int:
        return sum(week.get_potential_score() for week in self.weeks)

    def get_total_score(self) -> int:
        return sum(week.get_total_score() for week in self.weeks)


@dataclass
class Year(TimeUnit):
    year: int
    months: list[Month]

    def get_potential_score(self) -> int:
        return sum(month.get_potential_score() for month in self.months)

    def get_total_score(self) -> int:
        return sum(month.get_total_score() for month in self.months)

    def s_today(self) -> str:
        return f"{len(self.months[-1].weeks[-1].days)} {self.months[-1]} {self.year}"
