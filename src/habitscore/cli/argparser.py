"""Arg parsing class for CLI functionality"""

from argparse import ArgumentParser

from habitscore.cli.subparser import Subparser, AddSubparser, UpdateSubparser, DelSubparser


class ArgParser:
    """Parses console args"""

    def __init__(self):
        self.parsed_args: dict = dict()

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

    # Assign presets to days
    # Assign tasks (one-time) to days
    # Update progress
    # Print day's progress
    # Print history
    # Compare/stats/sort/analyze

    def parse_execute_args(self, args: list[str]):
        parsed_args = self._parser.parse_args(args)

        dict_args = parsed_args.__dict__
        self.parsed_args = dict_args

        print(dict_args)

    def validate_parsed_subparsers(self):
        for subparser in self.subparsers_o:
            if subparser.name in self.parsed_args.keys():
                subparser.validate_args()
