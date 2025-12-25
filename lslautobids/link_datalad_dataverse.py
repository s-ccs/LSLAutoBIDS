 
#import datalad_dataverse as dd

import subprocess
from pathlib import Path
from lslautobids.config_globals import cli_args, dataverse_base_url, bids_root
import os



def add_sibling_dataverse_in_folder(doi_id, logger):
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
    project_name = cli_args.project_name
    dataset_path = os.path.join(bids_root, project_name)
    try:
        # Change to the specified folder
        #os.chdir(folder_path)
        # Define the bash command as a list of strings
        command = ['datalad', 'add-sibling-dataverse', 
        #"-d", str(bids_dataset_path), 
        #"-s", sibling_name,
        "--existing", "reconfigure",
        dataverse_base_url,
        doi_id]
        # Call the bash command using subprocess.run()
        subprocess.run(command, check=True, cwd=dataset_path)
        logger.info("Sibling Dataverse added successfully!")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error occurred while running the command: {e}")
    except FileNotFoundError:
        logger.error("Error: The 'datalad' command is not found. Make sure Datalad is installed and accessible.")
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")

"""
from datalad.api import add_sibling_dataverse

def add_sibling_dataverse_in_folder(doi_id, project_name, logger):
    dataset_path = os.path.join(bids_root, project_name)
    add_sibling_dataverse(
        dv_url=dataverse_base_url,
        ds_pid=doi_id,
        dataset=dataset_path,
        existing='reconfigure',
    )
    logger.info("Sibling Dataverse added successfully!")
"""