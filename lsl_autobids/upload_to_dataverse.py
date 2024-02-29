import subprocess
import os


def push_files_to_dataverse():

        # Define the bash command as a list of strings
        command = ['datalad', 'push', '--to' , 'dataverse']
        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True)
        print("Uploaded to dataverse successfully!")