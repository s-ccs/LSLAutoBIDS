import argparse
import os
from processing import check_for_new_data
import yaml
import tomllib
import toml


def parse_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

def check_for_project(project_name,project_root,projects,bids_root,project_stim_root):
    """
    Checks if the project exists in the PROJECTS list
    """
    if project_name in projects:
        project_path = os.path.join(project_root,project_name)
        if not os.path.exists(project_path):
            print('Project not found')
            exit() 
        print('Project found')

        user_input = input("Do you want to check for the data in the project? (y/n): ")

        if user_input.lower() == "y":
            check_for_new_data(project_root,project_name, bids_root,project_stim_root)
        elif user_input.lower() == "n":
            print("Program aborted.")
        else:
            print("Invalid Input.")
        
    else: 
        print('Project name not specified correctly')
        exit()

def list_directories(path):
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories

def main():

    # Argument parser
    argparser = argparse.ArgumentParser(description='Get the project name')
    argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    #argparser.add_argument('-c','--config_file', type=str, help='Enter the path to the config file')
    args = argparser.parse_args()
    

    #get the config file and parse it
    config_file = './config/config.yaml'
    config = parse_yaml_file(config_file)
    project_root = os.path.join(os.path.expanduser("~"),config['PROJECT_ROOT'])
    bids_root = os.path.join(os.path.expanduser("~"),config['BIDS_ROOT'])
    project_stim_root = os.path.join(os.path.expanduser("~"),config['PROJECTS_STIM_ROOT'])
    projects = list_directories(project_root)
    

    # get the project name and check if the project exists
    project_name = args.project_name
    project_toml_path = os.path.join(project_root,project_name,project_name+'_config.toml')
    with open(project_toml_path, 'rb') as file:
        data = tomllib.load(file)
        data['Dataset']['title'] = project_name
        f = open(project_toml_path,'w')
        toml.dump(data, f)
        f.close()

    check_for_project(project_name,project_root, projects, bids_root,project_stim_root)



if __name__ == "__main__":
    main()  
