# imports
import os
import logging
from typing import List, Union
from utils import get_user_input, read_toml_file
from convert_to_bids_and_upload import  bids_process_and_upload
from config_globals import cli_args, project_root
import toml


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def process_new_files(file_status: List[str]) -> None:
    """Processes new .xdf files and prompts user to convert/upload.

    Args:
        file_status (List[str]): List of new files detected.
    """

    logger.info("Processing new files...")
    # set up global variables
    project_name = cli_args.project_name
    processed_files = []
    for file_path in file_status:
        if file_path.endswith('.xdf'):
            
            # This code is to handle the recordings from the same session and same subject
            # Remove "_old" from the filename if present
            _, file_name = os.path.split(file_path)
            file_name_no_ext, ext = os.path.splitext(file_name)
            if file_name_no_ext.endswith('_old'):
                logger.error(f"File '{file_name}' appears to be a duplicate. It ends with '_old'. Please manually check the file.")
                raise RuntimeError("File overwrite declined by user.")

            processed_files.append(file_name_no_ext + ext)
    
    logger.info(f"Processed files: {processed_files}")

    # User prompt asking if we want to proceed to convert and upload
    if cli_args.yes:
        # Automatically proceed without asking
        logger.info("Automatically proceeding with BIDS conversion.")    
    else:
        user_choice = get_user_input("Do you want to proceed with BIDS conversion?")
        if user_choice == 'n':
            logger.warning("User aborted BIDS conversion.")
            _clear_last_run_log(project_name)
            raise RuntimeError("BIDS conversion aborted by user.")

    logger.info("Starting BIDS conversion.")
    bids_process_and_upload(processed_files)


def _clear_last_run_log() -> None:
    """Clears the last run log file for the given project.
    """
    project_name = cli_args.project_name
    log_path = os.path.join(project_root, project_name, "last_run_log.txt")
    try:
        with open(log_path, 'w') as f:
            f.truncate(0)
        logger.info("Cleared last run log.")
    except Exception as e:
        logger.error(f"Failed to clear log: {e}")


def check_for_new_files(path: str, ignore_subjects) -> Union[List[str], str]:
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
    
    for dirpath, dirnames, filenames in os.walk(path):
        # Skip the root directory
        if dirpath == path:
            # Modify dirnames in-place to exclude ignored subjects
            dirnames[:] = [d for d in dirnames if d not in ignore_subjects]
            continue

        # Skip if the current dirpath includes any ignored subject
        if any(ignored in dirpath.split(os.sep) for ignored in ignore_subjects):
            logger.info(f"Skipping directory {dirpath} due to ignored subjects.")   
            continue

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.getmtime(file_path) > last_run_time:
                new_files.append(file_path)

    return new_files if new_files else 'No new files found'
    
def check_for_new_data() -> None:

    """Checks for new data files and triggers processing.
    """
    # set up global variables
    project_name = cli_args.project_name
    logger.info("Checking for new data...")

    # Keep a log of the files changes in a text file
    # last_checked_file_path = './last_time_checked.txt'
    project_path = os.path.join(project_root,project_name)

    toml_path = os.path.join(project_path, cli_args.project_name + '_config.toml')
    data = read_toml_file(toml_path)

    ignore_subjects = data["IgnoreSubjects"]["ignore_subjects"]

    logger.info("Ignored subjects: %s", ignore_subjects)
    file_status = check_for_new_files(project_path, ignore_subjects)    
    if file_status == 'No new files found':
        logger.info("No new files detected.")
        input("Press Enter to exit...")
        raise RuntimeError("No new files found.")
    else:
        logger.info(f"New files detected: {file_status}")
        process_new_files(file_status)


