 
#import datalad_dataverse as dd

import subprocess
import logging
from globals import dataverse_base_url

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def add_sibling_dataverse_in_folder(doi_id):
    """
    Adds a Dataverse repository as a sibling to the current Datalad dataset.

    This function runs the `datalad add-sibling-dataverse` command using the 
    given Dataverse DOI and a globally configured Dataverse base URL.

    Args:
        doi_id (str): The persistent identifier (DOI) of the Dataverse dataset.

    Raises:
        subprocess.CalledProcessError: If the subprocess command fails.
        FileNotFoundError: If the `datalad` command is not found in the environment.
        Exception: For any other unexpected errors.
    """
    try:
        # Change to the specified folder
        #os.chdir(folder_path)

        # Define the bash command as a list of strings
        command = ['datalad', 'add-sibling-dataverse', dataverse_base_url,doi_id]
        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True)
        logger.info("Sibling Dataverse added successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running the command: {e}")
    except FileNotFoundError:
        logger.error("Error: The 'datalad' command is not found. Make sure Datalad is installed and accessible.")
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")

