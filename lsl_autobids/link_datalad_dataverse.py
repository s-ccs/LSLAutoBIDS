 
#import datalad_dataverse as dd

import subprocess
import os
from globals import dataverse_base_url
import toml


def add_sibling_dataverse_in_folder(doi_id):
    try:
        # Change to the specified folder
        #os.chdir(folder_path)

        # Define the bash command as a list of strings
        command = ['datalad', 'add-sibling-dataverse', dataverse_base_url,doi_id]
        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True)
        print("Sibling Dataverse added successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the command: {e}")
    except FileNotFoundError:
        print("Error: The 'datalad' command is not found. Make sure Datalad is installed and accessible.")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

