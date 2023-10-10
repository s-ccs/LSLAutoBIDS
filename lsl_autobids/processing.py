import os
import time
import warnings
import sys
from bids import BIDS
from folder_config import BIDS_ROOT
from main import PROJECT_NAME
bd = BIDS()

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
            _, file_name = os.path.split(file_path)
            file_name_without_ext, ext = os.path.splitext(file_name)
            if file_name_without_ext.endswith('_old'):
                warning_message = "WARNING: The file already exists. It might be an old file. Are you sure you want to overwrite it? (y/n): "
                while True:
                    user_response = input(warning_message)
                    if user_response.lower() == 'n':
                        warnings.warn("Operation aborted. File will not be overwritten. Please check the file again!", UserWarning)
                        sys.exit()
                    elif user_response.lower() == 'y':
                        print('Operation resumed. File will be overwritten in Dataverse with the new file....')
                        break
                    else:
                        print('Invalid response. Please enter "y" for yes or "n" for no.')

                # Skip adding the file with the _old to processed_files if the user chooses to overwrite
                if user_response.lower() == 'y':
                    continue  
            processed_files.append(file_name_without_ext + ext)
        
        
    # Loop over the processed files
    for file_name in processed_files:
        # get the subject_id and session_id from the file name
        subject_id = file_name.split('_')[0]
        session_id = file_name.split('_')[1]
        # Make the subject directory
        directory = BIDS_ROOT + PROJECT_NAME + '/' + subject_id + '/' + session_id + '/eeg'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # get the xdf path  from the project path and the file name
        xdf_path = os.path.join(project_path +'/' + subject_id+'/'+session_id+'/eeg',file_name)
        print(xdf_path)
        print(subject_id[-3:])
        bd.convert_to_bids(xdf_path,subject_id,session_id)


def check_for_new_files(function_path):

    # TODO - Alternative way of checking for new data
    # 1. Use Watchdog to monitor the project directory for new files
    # 2. Use the time.time() function to get the current time to then check for new files.
    # Used log filwe so that we can track the last time the script was run.
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
    This function checks for new data by comparing the current state of the PROJECT ROOT directory with the last checked
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