import subprocess
import os
import time
from globals import project_root


def push_files_to_dataverse(project_name):

        # Define the bash command as a list of strings
        command = ['datalad', 'push', '--to' , 'dataverse']
        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True)
        print("Uploaded to dataverse successfully!")

        # Save the current time as the last run time in the log file
        log_file_path = os.path.join(project_root,project_name, 'last_run_log.txt')
        current_time = time.time()
        with open(log_file_path, 'w') as f:
                f.write(str(current_time))