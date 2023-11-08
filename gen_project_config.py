import os
import argparse
import yaml

def parse_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None


argparser = argparse.ArgumentParser(description='Get the project name')
argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
args = argparser.parse_args()

# get the project name and check if the project exists
project_name = args.project_name

# get the config file and parse it
 #get the config file and parse it
config_file = 'data_config.yaml'
config = parse_yaml_file(config_file)
project_root = config['PROJECT_ROOT']
bids_root = config['BIDS_ROOT']
project_stim_root = config['PROJECTS_STIM_ROOT']


# Define the content for the TOML template
toml_content = """
# This is the project configuration file - This configuration can be customized for each project
[Authors]
  authors = "John Doe, Lina Doe"
[AuthorsContact]
  email = "john@gmail.com"
[Dataset]
  title = "Convert XDF to BIDS"
  dataset_description = "This is a test project to set up the pipeline to convert XDF to BIDS."
  License = "MIT License"
  taskName = "task-1"

[Sources]
  EEG = "EEGstream EE225"
  marker = ["LSL_Markers","eegoSports-EE225_markersMarkers"]

[Computers]
  stimulusComputerUsed = true

[Subject]
  subject = ["Medicine, Health and Life Sciences","Engineering"]

[Dataverse]
  dataset_id = 123456
  dataset_title = 'Convert XDF to BIDS'
  pid = 'doi:10.18234'
"""

# Define the path to the folder where you want to save the TOML file
folder_path = project_root + project_name +'/'

# Define the file name for the TOML file
file_name = 'lsl_autobids_project.toml'
path = folder_path + file_name
home_dir = os.path.expanduser("~")

# Combine the folder path and file name to create the full file path
file_path = os.path.join(home_dir, path)

# Check if the folder exists, and if not, create it
if not os.path.exists(os.path.join(home_dir, folder_path)):
    print(f'Creating folder: {folder_path}')
    os.makedirs(os.path.join(home_dir, folder_path))

# Write the TOML content to the file
with open(file_path, 'w') as toml_file:
    toml_file.write(toml_content)

print(f'Template TOML file saved at: {file_path}')
print('\n Please edit the TOML file to customize the project metadata.')

