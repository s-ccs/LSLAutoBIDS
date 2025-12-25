import subprocess
import os
import time
from lslautobids.config_globals import cli_args,project_root
from lslautobids.config_globals import bids_root
from pathlib import Path
import logging
import sys

def push_files_to_dataverse(project_name, logger):
        """     
    Pushes files from the current Datalad dataset to a linked Dataverse repository.

    This function executes the `datalad push --to dataverse` command and logs the operation.
    It also stores the current timestamp in a log file named 'last_run_log.txt' 
    inside the specified project's directory.

    Args:
        project_name (str): The name of the project whose dataset is being pushed.

    Raises:
        subprocess.CalledProcessError: If the Datalad push command fails.
        FileNotFoundError: If the target directory or files are not found.
        Exception: For any other unexpected errors during the process.
    """

        try:    
                project_name = cli_args.project_name
                dataset_path = os.path.join(bids_root, project_name) 
                # Define the bash command as a list of strings
                command = ['datalad', 'push', '--to' , 'dataverse']
                # Call the bash command using subprocess.run()
                subprocess.run(command, check=True, cwd=dataset_path)
                logger.info("Uploaded to dataverse successfully!")

                # Save the current time as the last run time in the log file
                log_file_path = os.path.join(project_root,project_name, 'last_run_log.txt')
                current_time = time.time()
                with open(log_file_path, 'w') as f:
                        f.write(str(current_time))
        except subprocess.CalledProcessError as e:
                logger.error(f"Datalad push command failed: {e}")
                raise
        except FileNotFoundError as e:
                logger.error(f"File or directory not found: {e}")
                raise
        except Exception as ex:
                logger.error(f"An unexpected error occurred: {ex}")
                raise