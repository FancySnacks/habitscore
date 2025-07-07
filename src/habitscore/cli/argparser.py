"""Arg parsing class for CLI functionality"""

from abc import ABC, abstractmethod
from argparse import ArgumentParser

from habitscore.task import EMeasurement, TASK_SCORE_RANGE


MEASUREMENT_OPTIONS: list[str] = list(EMeasurement)


class ArgParser:
    def __init__(self):
        self._parser = ArgumentParser(prog="Habitscore",
                                      description="Example desc",
                                      epilog="FancySnacks 2025"
                                      )

        self._parser.add_argument('--gui',
                                  action='store_true',
                                  help="Open the program in a GUI mode")

        self.subparsers = self._parser.add_subparsers(help='Subcommand help')

        self.subparsers_o: list[Subparser] = []
        self.subparsers_o.append(AddSubparser(self))
        self.subparsers_o.append(DelSubparser(self))
        self.subparsers_o.append(UpdateSubparser(self))

    # ArgExecutor for adding, deleting, updating
    # Factory pattern for creating subparsers of the same subparser parent

    # Assign presets to days
    # Assign tasks (one-time) to days
    # Update progress
    # Print day's progress
    # Print history
    # Compare/stats/sort/analyze

    def parse_execute_args(self, args: list[str]):
        parsed_args = self._parser.parse_args(args)
        dict_args = parsed_args.__dict__
        print(dict_args)


class Subparser(ABC):
    def __init__(self, parent: ArgParser, name: str, help_text: str):
        self.parent = parent
        self._parser = self.parent.subparsers.add_parser(name, help=help_text)
        self.subparsers = self._parser.add_subparsers(dest='item', required=True, help='Item type')
        self.setup_args()

    @abstractmethod
    def setup_args(self):
        pass


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
