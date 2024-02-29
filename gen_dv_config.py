import yaml
import os
import argparse
""" 
This is the configuration file for the dataverse project.
Description about the fields:
BIDS_ROOT: Set up the BIDS output path - it is referenced from the home directory of your PC. 
For example, if your home directory is /home/username and you have a data/bids directory where you have the BIDS data in the home directory then the BIDS_ROOT path will be 'data/bids/'
PROJECT_ROOT: This is the actual path to the directory containing xdf files
PROJECTS_STIM_ROOT: This is the actual path to the directory containing the stimulus files
BASE_URL: The base URL for the dataverse service.
API_TOKEN: Your API token for authentication - you can get it from the dataverse service.
PARENT_DATAVERSE_NAME: The name of the program or service.
"""
# Create a dictionary representing the template data with comments
template_data = {
    "BIDS_ROOT": "workspace/projects/LSLAutoBIDS/data/bids/",       
    "PROJECT_ROOT" : "workspace/projects/LSLAutoBIDS/data/projects/", 
    "PROJECTS_STIM_ROOT" : "workspace/projects/LSLAutoBIDS/data/project_stimulus/", 
    "BASE_URL": "https://darus.uni-stuttgart.de",  # The base URL for the service.
    "API_TOKEN": "# Paste your API token here",    # Your API token for authentication.
    "PARENT_DATAVERSE_NAME": "simtech_pn7_computational_cognitive_science"     # The name of the program or service.
}

argparser = argparse.ArgumentParser(description='Get the config path')
argparser.add_argument('-p','--configpath', default=os.path.join(os.path.expanduser("~"),'dataverse_projects_config'),type=str, help='Enter the config path')
args = argparser.parse_args()

# Specify the filename for the YAML file
config_path =args.configpath 

# Check if the config file exists, if yes, then ask the user permission to view the fields of the yaml file and ask if they want to overwrite the file
try:
    with open(config_path, "r") as template_file:
        print(f"The file '{config_path}' already exists.")
        print("Do you want to view the fields of the file? (yes/no): ")
        view = input()
        if view.lower() == "yes":
            print("The fields of the file are:")
            print(template_file.read())
        else:
            print("The fields of the file will not be displayed.")
        print("Do you want to overwrite the file? (yes/no): ")
        overwrite = input()
        if overwrite.lower() == "yes":
            print("The file will be overwritten.")
        else:
            print("The file will not be overwritten.")
            exit()
except FileNotFoundError:
    # Write the template data to the YAML file
    with open(config_path, "w") as template_file:
        yaml.dump(template_data, template_file)

    print(f"Template YAML file '{config_path}' has been created.")