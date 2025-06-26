"""Day tasks and functionality around them"""

from __future__ import annotations

import json

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import StrEnum, auto


class TaskCategory(StrEnum):
    HEALTH = auto()
    BODY = auto()
    MIND = auto()
    WORK = auto()
    HOBBIES = auto()
    OTHER = auto()


class Measurement(ABC):
    @abstractmethod
    def is_completed(self) -> bool:
        pass

    @abstractmethod
    def get_progress(self) -> str:
        pass

    @abstractmethod
    def to_json(self) -> dict:
        pass

    @abstractmethod
    def complete_task(self):
        pass

    def add_progress(self, progress: int):
        pass

    def to_json_template(self) -> dict:
        pass


class Completion(Measurement):
    def __init__(self):
        super().__init__()
        self.completed = False

    def complete_task(self):
        self.completed = True

    def is_completed(self) -> bool:
        return self.completed is True

    def get_progress(self) -> str:
        return "COMPLETED" if self.completed else "UNCOMPLETED"

    def to_json(self) -> dict:
        return {"type": "completion",
                "completed": self.completed}

    def to_json_template(self) -> dict:
        return {"type": "completion"}


class Count(Measurement):
    def __init__(self, goal: int, **kwargs):
        super().__init__()
        self.goal: int = goal
        self.current_progress: int = 0

    def complete_task(self):
        self.current_progress = self.goal

    def add_progress(self, progress: int):
        self.current_progress += progress

    def is_completed(self) -> bool:
        return self.current_progress >= self.goal

    def get_progress(self) -> str:
        return f"{self.current_progress}/{self.goal}"

    def to_json(self) -> dict:
        return {"type": "count",
                "goal": self.goal,
                "current_progress": self.current_progress}

    def to_json_template(self) -> dict:
        data = self.to_json()
        data.pop('current_progress')
        return data


class EMeasurement(StrEnum):
    COMPLETION = auto()
    COUNT = auto()

    @classmethod
    def from_json(cls, json_data: dict) -> Measurement:
        o = json_data['measurement']
        match o.pop('type').lower():
            case "completion":
                return Completion()
            case _:
                return Count(**o)


@dataclass(order=True, eq=True)
class Task:
    sort_index: int = field(init=False, repr=False)
    name: str
    _score: int
    measurement: Measurement
    category: TaskCategory

    def __post_init__(self):
        self.sort_index = self.score

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, new_score: int):
        if -1 < new_score < 6:
            self._score = new_score
        else:
            raise ValueError("Productivity score must be in range of 0-5")

    @property
    def is_completed(self) -> bool:
        return self.measurement.is_completed()

    @property
    def get_progress(self) -> str:
        return self.measurement.get_progress()

    def complete_task(self):
        self.measurement.complete_task()

    def to_json(self) -> dict:
        return {"name": self.name,
                "category": self.category,
                "_score": self.score,
                "measurement": self.measurement.to_json()}

    def to_json_template(self) -> dict:
        data = self.to_json()
        data['measurement'] = self.measurement.to_json_template()
        return data

    def __repr__(self) -> str:
        return f"[{self.category:<10}] {self.name:<20} [{self.is_completed}]"


@dataclass
class TaskPreset:
    name: str
    tasks: list[Task]

    def complete_task_by_name(self, name: str):
        task_to_complete = self.get_task_by_name(name)
        task_to_complete.complete_task()

    def get_task_by_name(self, name: str) -> Task:
        for task in self.tasks:
            if task.name == name:
                return task

        raise Exception("Task not found")

    def to_json(self):
        tasks = [task.to_json() for task in self.tasks]
        return {"name": self.name,
                "tasks": tasks}

    @classmethod
    def preset_from_file(cls, filepath: str) -> TaskPreset:
        with open(filepath, 'r') as file:
            json_data = json.load(file)

            tasks: list[Task] = []

            for task_data in json_data['tasks']:
                m = EMeasurement.from_json(task_data)
                task_data.pop('measurement')
                tasks.append(Task(**task_data, measurement=m))

            task_preset = TaskPreset(json_data['name'], tasks)

        return task_preset
