import argparse
import os
import time
from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath, print_dir_tree
import argparse
import requests
import json
import sys
import contextlib



# Set up the BIDS output path - Set all the Global variables
BIDS_ROOT = './BIDS/'


def load_config(config_file):
    """
    Loads the configuration file and returns the credentials.
    
    Parameters:
        config_file (str): The path to the configuration file.
    
    Returns:
        dict: A dictionary containing the credentials.
    """
    with open(config_file, "r") as file:
        config = json.load(file)
    return config

# Example usage
config_file = "darus_config.json"
config = load_config(config_file)

# DaRUS credentials
API_URL = config["api_url"]
API_TOKEN = config["api_token"]
DOI_ID = config["doi_id"]


def upload_to_darus(file_path):
    """
    Uploads a file to Dataverse using the Dataverse API.
    
    Parameters:
        api_url (str): The base URL of the Dataverse API.
        api_token (str): The API token for authentication.
        dataset_id (str): The ID of the dataset in which to upload the file.
        file_path (str): The path to the file to upload.
    """
    url = f"{API_URL}/api/datasets/{DOI_ID}/add"
    headers = {"Content-Type": "application/json", "X-Dataverse-key": API_TOKEN}
    
    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, files={"file": file})
        
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
    return 0

def validate_bids(bids_path):
    file_paths = []
    root_directory = os.path.abspath(bids_path)
    
    for root, _, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            if root == root_directory:

                # Validate BIDS for files in the root directory
                res = BIDSValidator().is_bids(file)
            else:
                # Modify file path to be relative to the root directory
                relative_path = os.path.relpath(file_path, root_directory)
                print(relative_path)
                res = BIDSValidator().is_bids('/'+relative_path)
            
            file_paths.append(res)  
    
    if all(file_paths):
        print("BIDS format is valid.")
        print('Uploading to DARUS......')
        # Perform additional actions such as uploading to darus
        #upload_to_darus(bids_path)
    else:
        print("Invalid BIDS format.")
    


# Load the xdf file from the given path and get its streams    
def get_the_streams(xdf_path):
    """
    Retrieve the stream names and information from an XDF file.

    Parameters:
    xdf_path (str): The path to the XDF file.

    Returns:
    tuple: A tuple containing the stream names and the stream information.

    """
       
    
    streams = resolve_streams(xdf_path)
    
    stream_names = [streams[i]['name'] for i in range(len(streams))]
    return stream_names,streams


def create_raw_xdf(xdf_path,streams):
    """
    Create a raw object from an XDF file containing specific streams.

    Parameters:
    xdf_path (str): The path to the XDF file.
    streams (list): A list representing the streams extracted from the xdf file.

    Returns:
    mne.io.RawXDF: The raw object created from the XDF file.

    """
    # Get the stream id of the EEG stream
    stream_id = match_streaminfos(streams, [{"type": "EEG"}])[0]
    raw = read_raw_xdf(xdf_path,stream_ids=[stream_id])
    return raw


def convert_to_bids(xdf_file,subject_id,session_id):
    
    print("Converting to BIDS........") 
    # Create the new raw file from xdf file
    _,streams = get_the_streams(xdf_file)
    raw = create_raw_xdf(xdf_file,streams)

    # Get the bidspath for the raw file
    bids_path = BIDSPath(subject=subject_id[-3:], 
                         session=session_id[-3:], 
                         run=None, task=PROJECT_NAME, 
                         root=BIDS_ROOT, 
                         datatype='eeg', 
                         suffix='eeg', 
                         extension='.vhdr')
    
    # Write the raw data to BIDS in BrainVision format
    write_raw_bids(raw, bids_path, overwrite=True, verbose=True,format='BrainVision',allow_preload=True)

    # Validate the BIDS data
    validate_bids(BIDS_ROOT)


def proceesing_new_files(file_status,project_path):
    """
    Processes the new files with the ".xdf" extension, adding the file names (without "_old") to a list.
    
    Parameters:
        file_status (list): A list of file paths.
    """
    print("Processing new files.........")
    processed_files = []
    for file_path in file_status:
        if file_path.endswith('.xdf'):
            
            # This code is to handle the recordings from the same session and same subject
            # Remove "_old" from the filename if present
            file_directory, file_name = os.path.split(file_path)
            file_name_without_ext, ext = os.path.splitext(file_name)
            if file_name_without_ext.endswith('_old'):
                file_name_without_ext = file_name_without_ext[:-4]
            
            processed_files.append(file_name_without_ext + ext)
        
    # Loop over the processed files
    for file_name in processed_files:
        # get the subject_id and session_id from the file name
        subject_id = file_name.split('_')[0]
        session_id = file_name.split('_')[1]
        # Make the subject directory
        directory = BIDS_ROOT + '/' + subject_id + '/' + session_id + '/eeg'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # get the xdf path  from the project path and the file name
        xdf_path = os.path.join(project_path +'/' + subject_id+'/'+session_id+'/eeg',file_name)
        print(xdf_path)
        print(subject_id[-3:])
        convert_to_bids(xdf_path,subject_id,session_id)

def check_for_new_files(function_path):
    """
    Checks for new files in a deep folder structure since the last run.
    
    Parameters:
        function_path (str): The path to the function directory.
    
    Returns:
        list: A list of new file paths.
    """
    # Get the path of the log file
    log_file_path = os.path.join(function_path, "last_run_log.txt")
    
    # Retrieve the last run time from the log file
    try:
        with open(log_file_path, 'r') as f:
            last_run_time = f.read().strip()
            if last_run_time:
                last_run_time = float(last_run_time)
            else:
                last_run_time = 0.0
    except FileNotFoundError:
        last_run_time = 0.0
    
    # Check for new files
    new_files = []
    for dirpath, _, filenames in os.walk(function_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.getmtime(file_path) > last_run_time:
                new_files.append(file_path)
    
    # Save the current time as the last run time in the log file
    current_time = time.time()
    with open(log_file_path, 'w') as f:
        f.write(str(current_time))
        
    if new_files:
        return new_files
    else:
        return 'No new files found'
    
def check_for_new_data(project_path):
    """
    This function checks for new data by comparing the current state of the BIDS_ROOT directory with the last checked
    state. If new files are found, further processing are done.
    
    """
    # Code to check for new data
    print("Checking for new data....")

    # Keep a log of the files changes in a text file
    #last_checked_file_path = './last_time_checked.txt'

    file_status = check_for_new_files(project_path)
    if file_status == 'No new files found':
        print('No new files detected.')
    else:
        print('New files detected....')
        proceesing_new_files(file_status,project_path)
        

PROJECTS_ROOT = './projects'
# Write an argument parser which takes the project name as argument while running the script
argparser = argparse.ArgumentParser(description='Get the project name')
# give a -p or --project_name argument to the script
argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
args = argparser.parse_args()

#take the project name and find the project in the project directory amd print project not found if the path doesnot exist
project_name = args.project_name
# make project name a global variable
PROJECT_NAME = project_name
project_path = os.path.join(PROJECTS_ROOT,PROJECT_NAME)
if not os.path.exists(project_path):
    print('Project not found')
    exit()      
check_for_new_data(project_path)




