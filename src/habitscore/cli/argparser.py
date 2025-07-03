"""Arg parsing class for CLI functionality"""

from argparse import ArgumentParser


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

        # ==== Add Subparser ==== #

        self.add_subparser = self.subparsers.add_parser('add', help='Add new Task, Task Preset or Task Category')
        self.subparsers_add = self.add_subparser.add_subparsers(help='Subcommand help')

        self.add_task_subparser = self.subparsers_add.add_parser('task', help='Add new Task')
        self.add_preset_subparser = self.subparsers_add.add_parser('preset', help='Add new Task')
        self.add_category_subparser = self.subparsers_add.add_parser('category', help='Add new Task')

        # ==== Delete Subparser ==== #

        self.del_subparser = self.subparsers.add_parser('del', help='Del target Task, Task Preset or Task Category')
        self.subparsers_del = self.del_subparser.add_subparsers(help='Subcommand help')

        self.del_task_subparser = self.subparsers_del.add_parser('task', help='Delete Task')
        self.del_preset_subparser = self.subparsers_del.add_parser('preset', help='Delete Preset')
        self.del_category_subparser = self.subparsers_del.add_parser('category', help='Delete Task Category')

        # ==== Update Subparser ==== #

        self.update_subparser = self.subparsers.add_parser('update',
                                                           help='Update attributes of target Task, Task Preset or '
                                                                'Task Category')
        self.subparsers_update = self.update_subparser.add_subparsers(help='Subcommand help')

        self.update_task_subparser = self.subparsers_update.add_parser('task', help='Update Task')
        self.update_preset_subparser = self.subparsers_update.add_parser('preset', help='Update Preset')
        self.update_category_subparser = self.subparsers_update.add_parser('category', help='Update Task Category')

    # ArgExecutor for adding, deleting, updating
    # Move subparsers into standalone classes

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
