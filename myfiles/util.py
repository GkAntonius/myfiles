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
