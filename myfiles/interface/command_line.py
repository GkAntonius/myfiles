from textwrap import dedent
from argparse import ArgumentParser
from .cli_functions import get_cli_functions

__all__ = ['command_line_execution']

def command_line_execution():

    parser = ArgumentParser(
        prog='myfiles', 
        description = 'Project management.',
        )   
    
    #parser.add_argument(
    #    '-d', '--dry-run', action='store_true',
    #    dest='dry_run',
    #    help="""Print command but don't do it.""",
    #    )

    subparsers = parser.add_subparsers(title='command', required=True)
    
    for func in get_cli_functions():
        func.add_parser(subparsers)

    args, other_args = parser.parse_known_args()
    args.func(args)
