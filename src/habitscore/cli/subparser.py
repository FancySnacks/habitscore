"""Subparser classes"""

from __future__ import annotations

from abc import ABC, abstractmethod
from argparse import ArgumentError
from typing import TYPE_CHECKING

from habitscore.task import TASK_SCORE_RANGE, EMeasurement

if TYPE_CHECKING:
    from habitscore.cli.argparser import ArgParser


MEASUREMENT_OPTIONS: list[str] = list(EMeasurement)


class Subparser(ABC):
    def __init__(self, parent: ArgParser, name: str, help_text: str):
        self.name = name
        self.parent = parent
        self._parser = self.parent.subparsers.add_parser(name, help=help_text)
        self.subparsers = self._parser.add_subparsers(dest='item', required=True, help='Item type')
        self.setup_args()

    @abstractmethod
    def setup_args(self):
        pass

    def validate_args(self) -> bool:
        return True


class AddSubparser(Subparser):
    def __init__(self, parent):
        super().__init__(parent, name='add', help_text='Add new Task or Task Preset')

    def setup_args(self):
        task = self.subparsers.add_parser('task', help='Add a new Task')
        task.add_argument('--name', required=True)
        task.add_argument('--category', type=str, required=True)
        task.add_argument('--score', type=int, choices=TASK_SCORE_RANGE, required=True)
        task.add_argument('--measurement', type=str, choices=MEASUREMENT_OPTIONS, required=True)
        task.add_argument('--goal', type=int, help="Required when --measurement is 'count'")

        preset = self.subparsers.add_parser('preset', help='Add a new Preset')
        preset.add_argument('--name', required=True)

    def validate_args(self):
        if self.parent.parsed_args['measurement'] == 'count':
            if self.parent.parsed_args.keys() is None:
                raise ArgumentError(argument=None,
                                    message="--measurement 'count' argument has to be used along with "
                                            "measurable --goal <value> arg!")
        else:
            self.parent.parsed_args.pop('goal')


class DelSubparser(Subparser):
    def __init__(self, parent):
        super().__init__(parent, name='del', help_text='Delete target Task or Task Preset')

    def setup_args(self):
        task = self.subparsers.add_parser('task', help='Delete Task')
        task.add_argument('--name', required=True)

        preset = self.subparsers.add_parser('preset', help='Delete Preset')
        preset.add_argument('--name', required=True)


class UpdateSubparser(Subparser):
    def __init__(self, parent):
        super().__init__(parent, name='update', help_text='Update target Task or Task Preset')

    def setup_args(self):
        task = self.subparsers.add_parser('task', help='Update a Task')
        task.add_argument('--name', required=True)
        task.add_argument('--category', type=str)
        task.add_argument('--score', type=int, choices=TASK_SCORE_RANGE)
        task.add_argument('--measurement', type=str, choices=MEASUREMENT_OPTIONS)
        task.add_argument('--goal', type=int, help="Required when --measurement is 'count'")

        preset = self.subparsers.add_parser('preset', help='Update a Task Preset')
        preset.add_argument('--name', required=True)
