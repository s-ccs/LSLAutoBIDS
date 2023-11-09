import os
import time
import warnings
import sys
from convert_to_bids_and_upload import  bids_process_and_upload

def proceesing_new_files(file_status,project_root,project_name,bids_root, project_stim_root):
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
                        print('Operation resumed. File will be overwritten with the new file....')
                        break
                    else:
                        print('Invalid response. Please enter "y" for yes or "n" for no.')

                # Skip adding the file with the _old to processed_files if the user chooses to overwrite
                if user_response.lower() == 'y':
                    continue  
            processed_files.append(file_name_without_ext + ext)
    print("The processed files are: \n")
    print(processed_files)

    project_path = os.path.join(project_root,project_name)
    # Generate a user prompt asking if we want to proceed to convert and upload
    ask_convert_message = "Do you want to proceed for BIDS Conversion?"
    while True:
        user_response = input(ask_convert_message)
        
        if user_response.lower() == 'n':
            warnings.warn("Operation aborted. Files will not be converted.", UserWarning)
            file = os.path.join(project_path,"last_run_log.txt")
            with open(file, 'w') as file:
                file.truncate(0)
            sys.exit()
        elif user_response.lower() == 'y':
            print('Operation resumed. Files will be converted to BIDS.')
            break
        else:
            print('Invalid response. Please enter "y" for yes or "n" for no.')
   
    bids_process_and_upload(processed_files, bids_root, project_root, project_name, project_stim_root)

    # for file in processed_files:
    #     # get the subject id and the session id
    #     subject_id = file.split('_')[0]
    #     session_id = file.split('_')[1]
    #     # Make the subject directory
    #     full_path = os.path.join(bids_root, project_name , subject_id , session_id ,'eeg')
    #     if not os.path.exists(full_path):
    #         os.makedirs(full_path)
    #     #get the xdf path  from the project path and the file name
    #     xdf_path = os.path.join(project_path, subject_id, session_id,"eeg",file_name)
    #     # convert the xdf file to BIDS
        


    # # Make a text file to keep track of the processed files
    # processed_files_file_path = "processed_files.txt"
    # with open(processed_files_file_path, 'a') as f:
    #     for file_name in processed_files:
    #         # get the subject_id and session_id from the file name
    #         subject_id = file_name.split('_')[0]
    #         session_id = file_name.split('_')[1]
    #         # # Make the subject directory
    #         # full_path = bids_root + project_name + '/' + subject_id + '/' + session_id + '/eeg'
    #         # if not os.path.exists(full_path):
    #         #     os.makedirs(full_path)
    #         #get the xdf path  from the project path and the file name
    #         xdf_path = os.path.join(project_path +'/' + subject_id+'/'+session_id+'/eeg',file_name)
    #         f.write(xdf_path + '\n')
    
    # with open(processed_files_file_path, 'r') as f:
    #     lines = f.readlines()
    #     print("Number of files processed: ", len(lines))

   

def check_for_new_files(function_path):

    # TODO - Alternative way of checking for new data
    # 1. Use Watchdog to monitor the project directory for new files
    # 2. Use the time.time() function to get the current time to then check for new files.
    # Used log file so that we can track the last time the script was run.
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

    
    # Check for new files except the log file
    new_files = []
    for dirpath, _, filenames in os.walk(function_path):
        if dirpath == function_path:
            continue
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
    
def check_for_new_data(project_root, project_name, bids_root, project_stim_root):

    """
    This function checks for new data by comparing the current state of the PROJECT ROOT directory with the last checked
    state. If new files are found, further processing are done.
    
    """
    # Code to check for new data
    print("Checking for new data....")

    # Keep a log of the files changes in a text file
    # last_checked_file_path = './last_time_checked.txt'
    project_path = os.path.join(project_root,project_name)

    file_status = check_for_new_files(project_path)
    if file_status == 'No new files found':
        print('No new files detected.')
        input("Press Enter to exit...")
        sys.exit()
    else:
        print('New files detected....')
        proceesing_new_files(file_status,project_root, project_name, bids_root,project_stim_root)


