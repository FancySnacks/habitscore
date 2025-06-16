from __future__ import annotations

from dataclasses import dataclass
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


@dataclass
class Day(TimeUnit):
    name: str
    tasks: TaskPreset

    def get_potential_score(self) -> int:
        return sum(task.score for task in self.tasks.tasks)

    def get_total_score(self) -> int:
        return sum(task.score for task in self.tasks.tasks if task.is_completed)


@dataclass
class Week(TimeUnit):
    days: list[Day]

    def get_potential_score(self) -> int:
        return sum(day.get_potential_score() for day in self.days)

    def get_total_score(self) -> int:
        return sum(day.get_total_score() for day in self.days)


@dataclass
class Month(TimeUnit):
    index: int
    weeks: list[Week]

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

    def today(self) -> str:
        return f"{len(self.months[-1].weeks[-1].days)} {self.months[-1]} {self.year}"
