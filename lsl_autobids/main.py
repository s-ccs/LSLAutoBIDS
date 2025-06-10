#import packages
import argparse
import os
import toml
from config_globals import cli_args,project_root
import logging
from pathlib import Path
import sys
from utils import get_user_input, read_toml_file, write_toml_file
from processing_new_files import check_for_new_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)


def check_for_project(available_projects: list[str], project_name:str):
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
    update_project_config(project_path, project_name)

    if cli_args.yes:
        # Automatically proceed without asking
        check_for_new_data()
        print("Data check completed.")
    else:
        # Ask the user before proceeding
        user_input = get_user_input("Do you want to check for new data in the project folder? (y/n): ")
        if user_input == 'y':
            check_for_new_data()
            print("Data check completed.")
        else:
            print("Data check skipped by user.")
            sys.exit(0)
    # Ask the user if they want to check for new data
    

def list_directories(path: str) -> list:
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

def update_project_config(project_path: str, project_name: str):
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
    #config.setdefault('Dataset', {})['title'] = project_name 
    config['Dataset']['title'] = project_name
    logger.info("Updating project config with new project name...")

    write_toml_file(toml_path, config)
    logging.info(f"Updated project config for '{project_name}'.")


def main():
    
    """Main function to parse CLI arguments and trigger logic."""
    # Argument parser
    argparser = argparse.ArgumentParser(description="Check project and optionally update config.")
    argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    args = argparser.parse_args()

    try:
        try:
            available_projects = list_directories(project_root)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Failed to access project directory: {e}")
            sys.exit(1)
        project_path = check_for_project(args.project_name, available_projects)
        update_project_config(project_path, args.project_name)
    except Exception as e:
        logging.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()  
