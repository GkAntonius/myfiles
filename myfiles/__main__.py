import sys
if __name__ == '__main__':
    from .interface.command_line import command_line_execution
    sys.exit(command_line_execution())
