import yaml
import os
import argparse


def parse_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

""" 
This is the configuration file for the dataverse project.
Description about the fields:
BIDS_ROOT: Set up the BIDS output path - it is referenced from the home directory of your PC. 
For example, if your home directory is /home/username and you have a data/bids directory where you have the 
BIDS data in the home directory then the BIDS_ROOT path will be 'data/bids/'
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
argparser.add_argument('-p','--configpath', default=os.path.join(os.path.expanduser("~"),'autobids_config.yaml'),type=str, help='Enter the config path')
args = argparser.parse_args()

# Specify the filename for the YAML file
config_path =args.configpath 

# Save the configuration path to the config_info.yaml file
with open('./config_info.yaml') as f:
    data = yaml.safe_load(f)

data['CONFIG_PATH'] = config_path
with open('./config_info.yaml', 'w') as f:
    yaml.dump(data, f)


# Check if the config file exists, if yes, then ask the user permission to view the fields of the yaml file and ask if they want to overwrite the file
## HANDLE THE CASE NO SITUATION and ask repetedly until the user gives a valid input
try:
    with open(config_path, "r") as template_file:
        print(f"The file '{config_path}' already exists.")
        while True:
            print("Do you want to view the fields of the file? (yes/no): ")
            view = input()
            if view.lower() == "yes" or view.lower() == "y":
                print("The fields of the file are:")
                print(template_file.read())
                break
            elif view.lower() == "no" or view.lower() == "n":
                print("The fields of the file will not be displayed.")
                break
            else:
                print("Invalid input. Please enter a valid input.")
        while True:
            print("Do you want to overwrite the file? (yes/no): ")
            overwrite = input()
            if overwrite.lower() == "yes" or overwrite.lower() == "y":
                print("The file will be overwritten.")
                with open(config_path, "w") as template_file:
                    yaml.dump(template_data, template_file)
                print(f"Template YAML file '{config_path}' has been overwritten with the default template.")
                break
            elif overwrite.lower() == "no" or overwrite.lower() == "n":
                print("The file will not be overwritten.")
                break
            else:
                print("Invalid input. Please enter a valid input.")
except FileNotFoundError:
    # Write the template data to the YAML file
    with open(config_path, "w") as template_file:
        yaml.dump(template_data, template_file)

    print(f"Template YAML file '{config_path}' has been created.")