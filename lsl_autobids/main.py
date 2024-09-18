#import packages
import argparse
import os
from processing_new_files import check_for_new_data
import tomllib
import toml
from globals import project_root


    
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


def check_for_project(project_name,projects):
    """
    Checks if the project exists in the projects folder

    Parameters
    ----------
    project_name : str
        name of the project
    projects : list
        list of projects in the project_root
    
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
            check_for_new_data(project_name)
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

    # get the root directories for further processing
    projects = list_directories(project_root)
    
    # get the project name and check if the project exists
    project_name = args.project_name
    project_exist = check_for_project(project_name, projects)

    if project_exist:
        project_toml_path = os.path.join(project_root, project_name, project_name+'_config.toml')
        with open(project_toml_path, 'rb') as file:
            data = tomllib.load(file)
            data['Dataset']['title'] = project_name
            f = open(project_toml_path,'w')
            toml.dump(data, f)
            f.close()

if __name__ == "__main__":
    main()  
