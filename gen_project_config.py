import os
import argparse

argparser = argparse.ArgumentParser(description='Get the project name')
argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
args = argparser.parse_args()


# get the project name and check if the project exists
project_name = args.project_name

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
"""

# Define the path to the folder where you want to save the TOML file
folder_path = './data/projects/'+ project_name +'/'

# Define the file name for the TOML file
file_name = 'lsl_autobids_project.toml'

# Combine the folder path and file name to create the full file path
file_path = os.path.join(folder_path, file_name)

# Check if the folder exists, and if not, create it
if not os.path.exists(folder_path):
    print(f'Creating folder: {folder_path}')
    os.makedirs(folder_path)

# Write the TOML content to the file
with open(file_path, 'w') as toml_file:
    toml_file.write(toml_content)

print(f'Template TOML file saved at: {file_path}')


