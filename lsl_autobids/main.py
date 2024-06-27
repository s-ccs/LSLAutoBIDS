#import packages
import argparse
import os
from processing import check_for_new_data
import yaml
import tomllib
import toml


def parse_yaml_file(yaml_file):
    """
    Parse a YAML file and return the data

    Parameters
    ----------
    yaml_file : str
        Path to the root config YAML file

    Returns
    -------
    dict
        Data from the YAML file
    """
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None
        

def get_user_input_for_data_check():
    """
    Get the user input for checking the data in the project folder

    Parameters
    ----------
    None

    Returns
    -------
    str
        User input
    """


    user_input = input("Do you want to check for the data in the project folder? (y/n): ")
    valid_letters = set("yYnN")
    attempts = 3

    for attempt in range(attempts):
        user_input = input("Please enter a letter: ").strip()
        
        if len(user_input) == 1 and user_input in valid_letters:
            return user_input
        else:
            remaining_attempts = attempts - attempt - 1
            if remaining_attempts > 0:
                print(f"Invalid input. You have {remaining_attempts} attempt(s) remaining.")
            else:
                print("Invalid input. Exiting the program.")
                exit()


def check_for_project(project_name,project_root,projects,bids_root,project_stim_root):
    """
    Checks if the project exists in the projects folder

    Parameters
    ----------
    project_name : str
        name of the project
    project_root : str
        root directory of the projects
    projects : list
        list of projects in the project_root
    bids_root : str
        root directory of the BIDS data
    project_stim_root : str
        root directory of the stimulus data
    
    Returns
    -------
    None
    """
    if project_name in projects:
        project_path = os.path.join(project_root,project_name)
        if not os.path.exists(project_path):
            print(f'Project: {project_name} not found')
            print('Exiting program')
            exit() 
        print('Project found')

        user_input = get_user_input_for_data_check()

        if user_input=="y" or user_input=="Y":
            check_for_new_data(project_root,project_name, bids_root,project_stim_root)
            
        elif user_input == "n" or user_input == "N":
            print("Program aborted. Closing...")
            exit()
    else: 
        print('Project name not specified correctly')
        exit()
    return True


def list_directories(path):
    """
    List all the directories in the path

    Parameters
    ----------
    path : str
        Path to the directory
    Returns
    -------
    list
        List of directories
    """
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories


def main():

    # Argument parser
    argparser = argparse.ArgumentParser(description='Get the project name')
    argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    args = argparser.parse_args()
    
    # Get the config file path from the autobids_config.yaml file and parse the file
    config_file = os.path.join(os.path.expanduser("~"),'.config/lslautobids/autobids_config.yaml')
    config = parse_yaml_file(config_file)

    # get the root directories for further processing
    project_root = os.path.join(os.path.expanduser("~"),config['PROJECT_ROOT'])
    bids_root = os.path.join(os.path.expanduser("~"),config['BIDS_ROOT'])
    project_stim_root = os.path.join(os.path.expanduser("~"),config['PROJECTS_STIM_ROOT'])
    projects = list_directories(project_root)
    

    # get the project name and check if the project exists
    project_name = args.project_name
    project_exist =check_for_project(project_name,project_root, projects, bids_root,project_stim_root)

    if project_exist:
        project_toml_path = os.path.join(project_root,project_name,project_name+'_config.toml')
        with open(project_toml_path, 'rb') as file:
            data = tomllib.load(file)
            data['Dataset']['title'] = project_name
            f = open(project_toml_path,'w')
            toml.dump(data, f)
            f.close()

if __name__ == "__main__":
    main()  
