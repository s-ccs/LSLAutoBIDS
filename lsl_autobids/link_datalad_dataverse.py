 
#import datalad_dataverse as dd

import subprocess
import os
import json
from .folder_config import BIDS_ROOT


def add_sibling_dataverse_in_folder(folder_path,BASE_URL,doi_id):
    try:
        # Change to the specified folder
        os.chdir(folder_path)

        # Define the bash command as a list of strings
        command = ['datalad', 'add-sibling-dataverse', BASE_URL, doi_id]

        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True)
        print("Sibling Dataverse added successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the command: {e}")
    except FileNotFoundError:
        print("Error: The 'datalad' command is not found. Make sure Datalad is installed and accessible.")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

