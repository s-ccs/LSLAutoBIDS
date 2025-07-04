#import packages
import argparse
import os
from config_globals import cli_args,project_root, bids_root
import logging
from pathlib import Path
import sys
from utils import get_user_input, read_toml_file, write_toml_file
from processing_new_files import check_for_new_data
from config_logger import get_logger
import subprocess
from datetime import datetime


def check_for_project(available_projects: list[str], project_name:str, logger):
    """Checks if the project exists and optionally verifies for new data.

        Args:
            available_projects (list[str]): List of valid projects.

        Raises:
            FileNotFoundError: If the project directory does not exist.
            ValueError: If project name is not valid.
        """
    if project_name not in available_projects:
        raise ValueError(f"Project '{project_name}' is not available in the recordings.")
    
    project_path = Path(os.path.join(project_root, project_name))

    if not project_path.exists():
        raise FileNotFoundError(f"Project directory '{project_path}' does not exist.")
    logger.info(f"Project folder for {project_name} found.")
    
    # update the project name in the project configuration file
    update_project_config(project_path, project_name, logger)

    if cli_args.yes:
        # Automatically proceed without asking
        check_for_new_data(logger)
        print("Data check completed.")
    else:
        # Ask the user before proceeding
        user_input = get_user_input("Do you want to check for new data in the project folder? (y/n): ",logger)
        if user_input == 'y':
            check_for_new_data(logger)
            print("Data check completed.")
        else:
            print("Data check skipped by user.")
            sys.exit(0)
   

def list_directories(path: str, logger) -> list:
    """List all directories at the given path.

    Args:
        path (str): The path to scan.

    Returns:
        list: List of directory names.

    Raises:
        FileNotFoundError: If the path does not exist.
        PermissionError: If access is denied.
    """
    try:
        return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    except FileNotFoundError:
        logger.error(f"The directory '{path}' was not found.")
        raise
    except PermissionError:
        logger.error(f"Permission denied when accessing '{path}'.")
        raise

def update_project_config(project_path: str, project_name: str, logger):
    """Updates the project TOML configuration file.

    Args:
        project_path (Path): Path to the project directory.
        project_name (str): Name of the project.

    Raises:
        FileNotFoundError: If the config file is missing.
    """
    toml_path = os.path.join(project_path, f"{project_name}_config.toml")
    if not Path(toml_path).exists():
        raise FileNotFoundError(f"Config file '{toml_path}' not found.")

    config = read_toml_file(toml_path)
    config['Dataset']['title'] = project_name
    logger.info("Updating project config with new project name...")

    write_toml_file(toml_path, config)
    logger.info(f"Updated project config for '{project_name}'.")


def main():
    
    """Main function to parse CLI arguments and trigger logic."""
    # Argument parser
    argparser = argparse.ArgumentParser(description="Check project and optionally update config.")
    argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    argparser.add_argument('-y','--yes', action='store_true', help='Automatically answer yes to all user prompts')
    argparser.add_argument('--redo_bids_conversion', action='store_true', help='Redo the entire BIDS conversion process from scratch for the processed files')
    argparser.add_argument('--redo_stim_pc', action='store_true', help='Redo the stim and physio processing for the processed files')
    args = argparser.parse_args()

    # Store args globally
    cli_args.init(args)
    
    project_name = cli_args.project_name

    def get_git_version():
        try:
            version = subprocess.check_output(["git", "describe", "--tags"], stderr=subprocess.DEVNULL).decode().strip()
            return version
        except Exception:
            return "unknown"

    ## NOTE : Make sure you have git tags.
    version = get_git_version()
    # make the log file if it does not exist
    log_path = os.path.join(bids_root, project_name, "code",f"{project_name}.log")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    def log_raw_line(log_path: str, message: str):
        with open(log_path, "a") as log_file:
            log_file.write(message + "\n")
    
    # Get the current time and format it
    curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Special logger without the general format
    log_raw_line(log_path, "\n" + "=" * 100)
    log_raw_line(log_path, f" LSLAutoBIDS | Version: {version} | Time: {curr_time}")
    log_raw_line(log_path, "=" * 100)
    # Initialize the logger AFTER cli_args is ready
    logger = get_logger(project_name, project_root)

    # Check if the stim flag is set in the toml file
    if args.redo_stim_pc:
        # get the stimulus flag from the toml file
        toml_path = os.path.join(project_root, project_name, f"{project_name}_config.toml")
        data = read_toml_file(toml_path)
        stim_flag = data['Computers']['stimulusComputerUsed']
        if not stim_flag:
            logger.warning("The stimulus computer flag is not set in the config file. Please set it to True to proceed with stim redo process.")
            sys.exit(1)

    try:
        try:
            available_projects = list_directories(project_root, logger)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Failed to access project directory: {e}")
            sys.exit(1)
        check_for_project(available_projects, project_name, logger)
       
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()  
