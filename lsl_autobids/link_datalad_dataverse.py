 
#import datalad_dataverse as dd
# TODO get the following data from the json file in dataverse_dataset_create.py
#ds = 'Computational Cognitive Science'
#ds_pid = 'doi:10.18419/darus-3520'
#url = 'https://darus.uni-stuttgart.de/'


import subprocess
import os

def add_sibling_dataverse_in_folder(folder_path):
    try:
        # Change to the specified folder
        os.chdir(folder_path)

        # Define the bash command as a list of strings
        command = ['datalad', 'add-sibling-dataverse', 'https://darus.uni-stuttgart.de/', 'doi:10.18419/darus-3520']

        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True)
        print("Sibling Dataverse added successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the command: {e}")
    except FileNotFoundError:
        print("Error: The 'datalad' command is not found. Make sure Datalad is installed and accessible.")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    folder_path = "./test_data"
    add_sibling_dataverse_in_folder(folder_path)