import subprocess

def prompt_user_and_run(command_parts):

    command = ' '.join(command_parts)
    print('Will execute the following command:')
    print(command)
    answer = input('Do you want to proceed? [y/N]: ')
    if answer.lower().startswith('y'):
        result = subprocess.run(
            command_parts,
            capture_output=False,
            text=True)
            # Check the return code
            #print("Return Code:", result.returncode)
            # Print the output
            #print("Output:", result.stdout)
            # Print the errors, if there are any
            #print("Error:", result.stderr)
            # Check for errors
            #if result.returncode != 0:
            #    print("Command failed.")
        return results
