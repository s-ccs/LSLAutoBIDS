#import packages
import argparse
import os
import tomllib
import toml
from globals import project_root
import logging
from pathlib import Path
import sys
from utils import get_user_input, read_toml_file
from processing_new_files import check_for_new_data

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

logger = logging.getLogger(__name__)


def check_for_project(project_name: str, available_projects: list[str]) -> Path:
    """Checks if the project exists and optionally verifies for new data.

        Args:
            project_name (str): Name of the project.
            available_projects (list[str]): List of valid projects.

        Returns:
            Path: The resolved path of the project.

        Raises:
            FileNotFoundError: If the project directory does not exist.
            ValueError: If project name is not valid.
        """
    if project_name not in available_projects:
        raise ValueError(f"Project '{project_name}' is not available in the recordings.")
    
    project_path = os.path.join(project_root, project_name)

    if not project_path.exists():
        raise FileNotFoundError(f"Project directory '{project_path}' does not exist.")
    
    logging.info(f"Project '{project_name}' found.")

    user_input = get_user_input("Do you want to check for new data in the project folder?")
    if user_input == 'y' :
        check_for_new_data(project_name)
    else:
        logging.info("Data check skipped by user.")
        sys.exit(0)

    return project_path
    

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

def update_project_config(project_path: Path, project_name: str):
    """Updates the project TOML configuration file.

    Args:
        project_path (Path): Path to the project directory.
        project_name (str): Name of the project.

    Raises:
        FileNotFoundError: If the config file is missing.
    """
    toml_path = os.path.join(project_path, f"{project_name}_config.toml")
    if not toml_path.exists():
        raise FileNotFoundError(f"Config file '{toml_path}' not found.")

    config = read_toml_file(toml_path)
    config.setdefault('Dataset', {})['title'] = project_name # data['Dataset']['title'] = project_name

    with toml_path.open("w", encoding="utf-8") as f:
        toml.dump(config, f)

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
