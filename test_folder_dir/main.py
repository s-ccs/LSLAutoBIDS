# Imports
import os
import time
from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath, print_dir_tree

# Set up the BIDS output path - Set all the Global variables
BIDS_ROOT = './test_data/BIDS/'


# Helper Functions

def check_for_new_file(folder_path, last_checked_file_path):
    """
    Checks for new files in a multilevel folder structure.
    
    Parameters:
        root_dir (str): The root directory to search for new files.
        last_checked_time (float): The last checked time in seconds since the epoch.
    
    Returns:
        list: A list of new file path or Invalid Path.
    """
    # Retrieve the last checked time from the file
    try:
        with open(last_checked_file_path, 'r') as f:
            last_checked_time = float(f.readlines()[-1].strip())

    except FileNotFoundError:
        last_checked_time = 0.0
    

    # Check for new files
    new_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.getmtime(file_path) > last_checked_time:
                new_files.append(file_path)
    
    # Save the current time to the file
    with open(last_checked_file_path, 'a') as f:
        f.write(str(time.time()) + '\n')
        
    if new_files != []:
        return new_files
    else:
        return 'No new files found'
    
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

# Upload to DARUS
def upload_to_darus(file_path):
    # Upload to DARUS
    # Set the DARUS upload path
    return 0


# Record or update the file in the database

def check_input_validity(number):
    """
    Check the validity of a number input and prompt for a valid three-digit number.

    Parameters:
    number (str): The number input to check.

    Returns:
    str: The valid three-digit number.

    """
    while True:
        if number.isdigit() and len(number) == 3:
            return number
        else:
            print("Invalid input!!")
            number = input("Enter a valid number: ")
            
def record_fresh_data():
    """
    Record fresh data and save it in the BrainVision BIDS format.

    This function prompts the user to enter the subject ID, session ID, and task name. 
    It then creates the necessary directory structure in the BIDS format, creates a raw object from an XDF file,
    and writes the raw data to BIDS in the BrainVision format.

    """

    # Code to record fresh data
    print("Recording fresh data...")
    
    # Get the subject inputs
    print('Enter the subject ID and the session ID in 00x format.')
    subject_id = check_input_validity(input("Enter the subject ID: "))
    print("Subject ID: ",subject_id)
    session_id = check_input_validity(input("Enter the session ID: "))
    print("Session ID: ",session_id)
    task = input("Enter the task name: ")
    print("Task: ",task)
    
    # Make the subject directory
    directory = BIDS_ROOT + 'sub-' + subject_id + '/ses-' + session_id + '/eeg'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # [TODO] Get the xdf file path 
    # The following is a placeholder
    ## Replace this with xdf file directory [Have to confirm what to check xdf file folder or BIDS folder]
    xdf_file = 'sample_data/raw_xdf/sub-004/ses-001/eeg/sub-004_ses-001_task-Duration_run-001_eeg.xdf'

    # Create the new raw file from xdf file
    _,streams = get_the_streams(xdf_file)
    raw = create_raw_xdf(xdf_file,streams)

    # Get the bidspath for the raw file
    bids_path = BIDSPath(subject=subject_id, 
                         session=session_id, 
                         run=None, task=task, 
                         root=BIDS_ROOT, 
                         datatype='eeg', 
                         suffix='eeg', 
                         extension='.vhdr')
    
    # Write the raw data to BIDS in BrainVision format
    write_raw_bids(raw, bids_path, overwrite=True, verbose=True,format='BrainVision',allow_preload=True)
    
    # Upload to DaRUS
    # Do you want to upload to DaRUS now

def check_for_new_data():
    """
    This function checks for new data by comparing the current state of the BIDS_ROOT directory with the last checked
    state. If new files are found, it uploads them to DaRUS. It also keeps a log of the file changes in a text file.
    
    """
    # Code to check for new data
    print("Checking for new data...")

    # Keep a log of the files changes in a text file
    last_checked_file_path = 'last_time_checked.txt'

    file_status = check_for_new_file(BIDS_ROOT, last_checked_file_path)
    if file_status == 'No new files found':
        print('No new upload to DaRUS')
    else:
        print('New upload to DaRUS detected')
        upload_to_darus(file_status)
        
        
# Main Function
def main():
    """
    Main function to interact with the user and perform actions based on user input.

    This function prompts the user to choose between recording fresh data or checking for new data. Based on the user's
    input, it calls the respective functions (`record_fresh_data` or `check_for_new_data`). The program continues to
    prompt for user input until the user chooses to quit by entering 'q'.

    """
    while True:
        user_input = input("Enter '1' to record fresh data or '2' to check for new data (press 'q' to quit): ")

        if user_input == '1':
            record_fresh_data()
        elif user_input == '2':
            check_for_new_data()
        elif user_input.lower() == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
