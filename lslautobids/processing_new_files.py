# imports
import os
from typing import List, Union
from lslautobids.utils import get_user_input, read_toml_file, write_toml_file
from lslautobids.convert_to_bids_and_upload import  bids_process_and_upload
from lslautobids.config_globals import cli_args, project_root
import re


def process_new_files(file_status: List[str],logger) -> None:
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
            if re.search(r'_old\d*$', file_name_no_ext):
                logger.error(f"File '{file_name}' appears to be a duplicate. It ends with an '_old' suffix. Please manually check the file.")
                raise RuntimeError("Duplicate file detected. Please check the file manually.")

            processed_files.append(file_name_no_ext + ext)
    
    logger.info(f"Processed files: {processed_files}")

    # extract tasks 
    tasks = []
    for file in processed_files:
        # Assuming the task is part of the filename, sub-888_ses-001_task-Default_run-001_eeg.xdf has task name 'task-default'
        parts = file.split('_')
        for part in parts:
            if part.startswith('task-'):
                task_name = part.split('-')[1]
                if task_name not in tasks:
                    tasks.append(task_name)

    # Append tasks to the project configuration file
    project_path = os.path.join(project_root, project_name)
    toml_path = os.path.join(project_path, project_name + '_config.toml')
    data = read_toml_file(toml_path)
   
    existing_tasks = set(data.get('Tasks', {}).get('tasks', []))

    # Add only new tasks
    updated_tasks = list(existing_tasks.union(tasks))

    # Save updated task list back to the config
    data['Tasks']['tasks'] = updated_tasks
    write_toml_file(toml_path, data)

    # User prompt asking if we want to proceed to convert and upload
    if cli_args.yes:
        # Automatically proceed without asking
        logger.info("Automatically proceeding with BIDS conversion.")    
    else:
        user_choice = get_user_input("Do you want to proceed with BIDS conversion?",logger)
        if user_choice == 'n':
            logger.warning("User aborted BIDS conversion.")
            raise RuntimeError("BIDS conversion aborted by user.")

    logger.info("Starting BIDS conversion.")
    bids_process_and_upload(processed_files, logger)

def _clear_last_run_log(logger) -> None:
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


def check_for_new_files(path: str, ignore_subjects, logger) -> Union[List[str], str]:
    """Checks for new files in the given folder structure since last run.

    Args:
        path (str): Directory path to scan.

    Returns:
        Union[List[str], str]: List of new file paths or a 'no files' message.
    """
    
    log_file_path = os.path.join(path, "last_run_log.txt")

    if cli_args.redo_bids_conversion:
        _clear_last_run_log(logger)

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
    
def check_for_new_data(logger) -> None:

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
    file_status = check_for_new_files(project_path, ignore_subjects, logger)
    ignore_tasks = data["Tasks"]["exclude_tasks"]

    filtered_files = [
    f for f in file_status
    if f.endswith('.xdf') and not any(f'task-{task}' in os.path.basename(f) for task in ignore_tasks)
    ]
    logger.info(f"Excluded files based on ignored tasks: {ignore_tasks}")
    if file_status == 'No new files found':
        logger.info("No new files detected.")
        input("Press Enter to exit...")
        raise RuntimeError("No new files found.")
    else:
        logger.info(f"New files detected: {filtered_files}")
        process_new_files(filtered_files, logger)


