import argparse
import os
#from processing import check_for_new_data
#from folder_config import *
import yaml


def parse_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

def check_for_project(project_name,PROJECTS,PROJECT_ROOT):
    """
    Checks if the project exists in the PROJECTS list
    """
    if project_name in PROJECTS:
        project_path = os.path.join(PROJECT_ROOT,project_name)
        if not os.path.exists(project_path):
            print('Project not found')
            exit() 
        print('Project found')
        #check_for_new_data(project_path)
    else: 
        print('Project name not specified correctly')
        exit()

def list_directories(path):
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories

def main():

    # TODO : Where do I keep the root location. Currently in folder_config.py
    # Argument parser
    argparser = argparse.ArgumentParser(description='Get the project name')
    argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    argparser.add_argument('-c','--config_file', type=str, help='Enter the path to the config file')
    args = argparser.parse_args()
    

    #get the config file and parse it
    config_file = args.config_file
    config = parse_yaml_file(config_file)
    PROJECT_ROOT = config['PROJECT_ROOT']
    PROJECTS_STIM_ROOT = config['PROJECTS_STIM_ROOT']
    BIDS_ROOT = config['BIDS_ROOT']
    PROJECTS = list_directories(PROJECT_ROOT)
    

    # get the project name and check if the project exists
    project_name = args.project_name
    check_for_project(project_name,PROJECTS,PROJECT_ROOT)


if __name__ == "__main__":
    main()  
