import os
import argparse
import yaml


# Define the content for the TOML template
toml_content = """
  # This is the project configuration file - This configuration can be customized for each project
  
  [AuthorsInfo]
    authors = "John Doe, Lina Doe" # List of authors separated by commas
    affiliation = "University of Stuttgart, University of Stuttgart" # Affiliation of the authors in the same order as authors
    email = "john@gmail.com" # Contact email of the authors in the same order as authors
  
  [DataverseDataset]
    title = "Convert XDF to BIDS" # Title of the  Dataverse dataset. This gets updated automatically by the project name.
    datasetDescription = "This is a test project to set up the pipeline to convert XDF to BIDS." # Description of the dataset. This description will appear in the dataset.json file which then eventually gets displayed in the dataverse metadata
    license = "MIT License" # License for the dataset, e.g. "CC0", "CC-BY-4.0", "ODC-By-1.0", "PDDL-1.0", "ODC-PDDL-1.0", "MIT License"
    subject = ["Medicine, Health and Life Sciences","Engineering"] # List of subjects related to the dataset required for dataverse metadata
    pid = '' # Persistent identifier for the dataset, e.g. DOI or Handle. This will be updated automatically after creating the dataset in dataverse.

  [OtherFilesInfo]
    otherFilesUsed = true # Set to true if you want to include other (non-eeg-files) files (experiment files, other modalities like eye tracking) in the dataset, else false
    expectedOtherFiles = [".edf", ".csv", "_labnotebook.tsv", "_participantform.tsv"] # List of expected other file extensions. Only the expected files will be copied to the beh folder in BIDS dataset. Give an empty list [] if you don't want any other files to be in the dataset. In this case only experiment files will be zipeed and copied to the misc folder in BIDS dataset.
  
  [SubjectInfo]
    ignoreSubjects = ['sub-777'] # List of subjects to ignore during the conversion - Leave empty to include all subjects. Changing this value will not delete already existing subjects.
    allTasks = [] # List of all possible tasks in the dataset. This will automatically be updated when new tasks are found during the conversion.
    excludeTasks = ['sampletask'] # List of tasks to exclude from the conversion for all subjects - Leave empty to include all tasks. Changing this value will not delete already existing tasks.
    anonymizationNumber = 123 # This is an anomization number that will be added to the recording date of all subjects.
    
  """



def parse_yaml_file(yaml_file):
    """
    Parse a YAML file and return the data

    Parameters
    ----------
    yaml_file : str
        Path to the YAML file
      
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
        


def main():

  # Get the project name from the user
  argparser = argparse.ArgumentParser(description='Get the project name')
  argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
  argparser.add_argument('-s','--standalone_toml', type=str, default='no', help= 'To enable the standalone toml file creation')
  argparser.add_argument('-c','--custom_dv_config', type=str, default=None, help='Optional path to a custom YAML config file')
  args = argparser.parse_args()

  print(f"ARGS: {args}")

  # Replace hardcoded path
  config_file = args.custom_dv_config or os.path.join(os.path.expanduser("~"),'.config/lslautobids/autobids_config.yaml')

  # get the project name and check if the project exists
  project_name = args.project_name
  standalone_toml = args.standalone_toml


  # Define the file name for the TOML file
  file_name = project_name + '_config.toml'

  if standalone_toml == 'yes':
      print('Creating standalone TOML file')
      file_path = file_name
  else:
    config = parse_yaml_file(config_file)
    project_root = config['PROJECT_ROOT']
    # Define the path to the folder where you want to save the TOML file
    folder_path = os.path.join(project_root, project_name)
    # Combine the folder path and file name to create the full file path
    file_path = os.path.join(os.path.expanduser("~"), folder_path,file_name)

    # Check if the folder exists, and if not, create it
    if not os.path.exists(os.path.join(os.path.expanduser("~"), folder_path)):
        print(f'Creating folder: {folder_path}')
        os.makedirs(os.path.join(os.path.expanduser("~"), folder_path))

  # Write the TOML content to the file
  with open(file_path, 'w') as toml_file:
      toml_file.write(toml_content)

  print(f'Template TOML file saved at: {file_path}')
  print('\n Please edit the TOML file to customize the project metadata before the conversion.')


if __name__ == "__main__":
    main()