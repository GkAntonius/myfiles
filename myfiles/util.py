import os
import subprocess

from enum import Enum, auto
class ScanResult(Enum):
        success = auto()
        failure = auto()
        no_scan = auto()
        #file_note_found = auto()
        #no_files = auto()
        #no_directories = auto()

def run_command(command_parts):
    command = ' '.join(command_parts)
    return os.system(command)

def prompt_user_confirmation(message):
    print(message)
    answer = input('Do you want to proceed? [y/N]: ')
    if answer.lower().startswith('y'):
        return True
    return False

def prompt_user_and_run(command_parts):

    command = ' '.join(command_parts)
    message = 'Will execute the following command:\n' + command
    if prompt_user_confirmation(message):
        result = os.system(command)

        # GA: This one doesnt work! Why??
        #result = subprocess.run(command_parts)

            #capture_output=True,text=True)
            # Check the return code
            #print("Return Code:", result.returncode)
            # Print the output
            #print("Output:", result.stdout)
            # Print the errors, if there are any
            #print("Error:", result.stderr)
            # Check for errors
            #if result.returncode != 0:
            #    print("Command failed.")
        return result

def rsync_level(n: int):
    """
    Get rsync arguments to exclude directories past a certain depts.
    A level of zero means only the files in the specified directory.
    A level of one means include subdirectories, and so on.
    """
    arguments = []
    if n < 0 or n > 10:
        return arguments

    arguments.append("--exclude=" + (n+1)*"*/")
    return arguments
    
def get_rsync_options(level=-1, files_only=False, with_filter=True,
                      dry_run=False, **kwargs):

    arguments = ['-avh']
    if with_filter:
        arguments.append('-F')

    if dry_run:
        arguments.append('-n')

    if files_only:
        level=1
    arguments.extend(rsync_level(level))

    return arguments

def get_rsync_command_parts(source, dest, **kwargs):
    options = get_rsync_options(**kwargs)
    command_parts = ["rsync", source, dest] + options
    return command_parts
