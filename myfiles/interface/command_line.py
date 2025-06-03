from textwrap import dedent
from argparse import ArgumentParser

from . import cli_functions

def command_line_execution():

    parser = ArgumentParser(
        prog='myfiles', 
        description = dedent(
        """\
        Project manager
        """),   
        #epilog = ("""Blob"""),
        )   
    
    parser.add_argument(
        'command', metavar='command',
        help= (
        """\
        Execute one of these commands:
            check_config
            check_project
            check_node
            show_nodes
            show_remote
            push_remote
            pull_remote
            push_scratch
            pull_scratch
            push_global_data
            push_local_data
            make_anadir
            save_results
            newproj
        """),
        default='check_project',
        #nargs = '*',
        choices = ('check_config', 'check_project', 'check_node',   
                   'check_nodes',
                   'check_remote',
                   'push_remote', 'pull_remote',
                   'push_scratch', 'pull_scratch',
                   'push_global_data', 'push_local_data',
                   'make_anadir',
                   'save_results',
                   'newproj',
            ),
        )
    
    parser.add_argument(
        '-d', '--dry-run', action='store_true',
        dest='dry_run',
        help="""Print command but don't do it.""",
        )

    # A very wacky way to do it...
    #args = parser.parse_args()
    args, other_args = parser.parse_known_args()
    func_name = args.command

    if func_name not in dir(cli_functions):
        print('Command not found: {func_name}')
        return

    func = getattr(cli_functions, func_name)
    result = func(*other_args)

    #g = globals()
    #if func_name in g:
    #    g[func_name](*other_args)
    #else:
    #    print('Command not found: {func_name}')
    #    print(g)

    #match func_name:
    #    case 'check_config':    
    #        check_config()
    #    case 'check_project':    
    #        check_project()
    #    case 'check_node':    
    #        check_node()
    #    case 'check_remote':    
    #        check_remote()
