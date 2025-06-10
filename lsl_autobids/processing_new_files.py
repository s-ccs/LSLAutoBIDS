# imports
import os
import logging
from typing import List, Union
from utils import get_user_input
from convert_to_bids_and_upload import  bids_process_and_upload
from globals import project_root


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def process_new_files(file_status: List[str], project_name: str) -> None:
    """Processes new .xdf files and prompts user to convert/upload.

    Args:
        file_status (List[str]): List of new files detected.
        project_name (str): Name of the current project.
    """

    logger.info("Processing new files...")
    processed_files = []
    for file_path in file_status:
        if file_path.endswith('.xdf'):
            
            # This code is to handle the recordings from the same session and same subject
            # Remove "_old" from the filename if present
            _, file_name = os.path.split(file_path)
            file_name_no_ext, ext = os.path.splitext(file_name)
            if file_name_no_ext.endswith('_old'):
                user_choice = get_user_input("WARNING: The file appears to be a duplicate ('_old'). Overwrite?")
                if user_choice == 'n':
                    logger.warning("User declined to overwrite file. Exiting.")
                    raise RuntimeError("File overwrite declined by user.")
                logger.info("Overwrite confirmed.")
                continue 
            processed_files.append(file_name_no_ext + ext)
    
    logger.info(f"Processed files: {processed_files}")

    # User prompt asking if we want to proceed to convert and upload
    if cli_args.yes:
        # Automatically proceed without asking
        logger.info("Automatically proceeding with BIDS conversion.")
        logger.info("Starting BIDS conversion.")
        bids_process_and_upload(processed_files)
    else:
        user_choice = get_user_input("Do you want to proceed with BIDS conversion?")
        if user_choice == 'n':
            logger.warning("User aborted BIDS conversion.")
            _clear_last_run_log(project_name)
            raise RuntimeError("BIDS conversion aborted by user.")

    logger.info("Starting BIDS conversion.")
    bids_process_and_upload(processed_files, project_name)


def _clear_last_run_log(project_name: str) -> None:
    """Clears the last run log file for the given project.

    Args:
        project_name (str): Name of the project.
    """
    log_path = os.path.join(project_root, project_name, "last_run_log.txt")
    try:
        with open(log_path, 'w') as f:
            f.truncate(0)
        logger.info("Cleared last run log.")
    except Exception as e:
        logger.error(f"Failed to clear log: {e}")


def check_for_new_files(path: str) -> Union[List[str], str]:
    """Checks for new files in the given folder structure since last run.

    Args:
        path (str): Directory path to scan.

    Returns:
        Union[List[str], str]: List of new file paths or a 'no files' message.
    """
    log_file_path = os.path.join(path, "last_run_log.txt")

    try:
        with open(log_file_path, 'r') as f:
            last_run = f.read().strip()
            last_run_time = float(last_run) if last_run else 0.0
    except FileNotFoundError:
        last_run_time = 0.0

    new_files = []
    for dirpath, _, filenames in os.walk(path):
        if dirpath == path:
            continue
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.getmtime(file_path) > last_run_time:
                new_files.append(file_path)

    return new_files if new_files else 'No new files found'
    
def check_for_new_data(project_name: str) -> None:

    """Checks for new data files and triggers processing.

    Args:
        project_name (str): Name of the project.
    """
    logger.info("Checking for new data...")

    # Keep a log of the files changes in a text file
    # last_checked_file_path = './last_time_checked.txt'
    project_path = os.path.join(project_root,project_name)
    file_status = check_for_new_files(project_path)
    if file_status == 'No new files found':
        logger.info("No new files detected.")
        input("Press Enter to exit...")
        raise RuntimeError("No new files found.")
    else:
        logger.info(f"New files detected: {file_status}")
        process_new_files(file_status, project_name)


