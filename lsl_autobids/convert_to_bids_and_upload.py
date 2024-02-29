from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath
import os
import shutil
from generate_dataset_json import generate_json_file
from dataverse_dataset_create import create_dataverse
from datalad_create import create_and_add_files_to_dataset
from link_datalad_dataverse import add_sibling_dataverse_in_folder
from upload_to_dataverse import push_files_to_dataverse
import toml
import yaml
import sys



class BIDS:
    def __init__(self):
        pass


    def get_the_streams(self, xdf_path):
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


    def copy_source_files_to_bids(self,xdf_file,subject_id,session_id,project_name,bids_root,projects_stim_root,stim):
        

        ### COPY THE SOURCE FILES TO BIDS ###
        # Get the source file name without the extension
        file_name = xdf_file.split(os.path.sep)[-1]
        file_name_without_ext, ext = os.path.splitext(file_name)
    
        
        # Copy the raw file
        new_filename = file_name_without_ext + '_raw' + ext
        
        # Destination path for the raw file
        dest_dir = os.path.join(bids_root , project_name , 'sourcedata' , subject_id , session_id , 'eeg')

        #check if the directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, new_filename)
        
        # Create a symbolic link with the new filename pointing to the source file
        try:
            os.symlink(xdf_file, dest_file) 
        except FileExistsError:
            pass

      
        if stim:
            ### COPY THE BEHAVIOURAL FILES TO BIDS ###
            # Copy the behavioral file - unique for all subjects
            print('Copying the behavioural files to BIDS........')
        
            # get the source path
            behavioural_path = os.path.join(projects_stim_root,project_name,subject_id,session_id)
            # get the destination path
            dest_dir = os.path.join(bids_root , project_name,  subject_id , session_id , 'beh')
            #check if the directory exists
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
        
            for file in os.listdir(behavioural_path):
                # remove the _eeg from the file_name_without_ext
                file_name_without_eeg = file_name_without_ext[:-4]
                new_filename = file_name_without_eeg + '_' + file
                dest_file = os.path.join(dest_dir, new_filename)
                try:
                    # Create a symbolic link with the new filename pointing to the source file
                    os.symlink(os.path.join(behavioural_path,file), dest_file)
                except FileExistsError:
                    pass
            
            ### COPY THE EXPERIMENT FILES TO BIDS ###

            # do the following steps only if others.zip doesnot exist
            print('Copying the experiment files to BIDS........')
        
            # Check if 'others.zip' exists
            zip_file_path = os.path.join(bids_root, project_name, 'others.zip')

            if not os.path.exists(zip_file_path):
                experiments_path = os.path.join(projects_stim_root,project_name,'experiment')
                # get the destination path
                dest_dir = os.path.join(bids_root , project_name, 'others')
                #check if the directory exists
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                for file in os.listdir(experiments_path):
                    src_file = os.path.join(experiments_path, file)
                    dest_file = os.path.join(dest_dir, file)
                    shutil.copy(src_file, dest_file)
                # Compress the 'other' directory into a ZIP file
                shutil.make_archive(dest_dir, 'zip', dest_dir)

                #Remove the original 'other' directory
                shutil.rmtree(dest_dir)
            else:
                print('Experiment files for the project already exist and hence not copied')

        print("Skipped copying the behvaioural and experiment files to BIDS.")

    def create_raw_xdf(self, xdf_path,streams):
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

    def convert_to_bids(self, xdf_path,subject_id,session_id,bids_root,project_name,project_stim_root,stim):
        print("Converting to BIDS........") 

        self.copy_source_files_to_bids(xdf_path,subject_id,session_id, project_name,bids_root,project_stim_root,stim)

        
        # Create the new raw file from xdf file
        _,streams = self.get_the_streams(xdf_path)
        raw = self.create_raw_xdf(xdf_path,streams)

        # Get the bidspath for the raw file
        bids_path = BIDSPath(subject=subject_id[-3:], 
                            session=session_id[-3:], 
                            run=None, task=project_name, 
                            root=bids_root+project_name, 
                            datatype='eeg', 
                            suffix='eeg', 
                            extension='.vhdr')
        
        # Write the raw data to BIDS in BrainVision format
        write_raw_bids(raw, bids_path, overwrite=True, verbose=True,format='BrainVision',allow_preload=True)

        print("Conversion to BIDS complete.")

        # print(' Validating the BIDS data........')
        # Validate the BIDS data
        val = self.validate_bids(bids_root+project_name,subject_id,session_id)
        return val
    
    def validate_bids(self,bids_path,subject_id,session_id):
        file_paths = []
        root_directory = os.path.abspath(bids_path)
        print(root_directory)
        
        for root, _, files in os.walk(root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip checking files with ".xdf" extension
                if file_path.endswith(".xdf"):
                    continue
                  
                # Ignore the zip files
                if file_path.endswith(".zip"):
                    continue

                # Ignore the files in the beh subdirectory
                if 'beh' in file_path:
                    continue
            
                #ignore the files starting with . (hidden files)
                if file.startswith('.'):
                    continue
                #ignore the .git directory altogether
                if '.git' in file_path:
                    continue

                if os.path.basename(root).startswith('.'):
                    continue               
                if root == root_directory:

                    # Validate BIDS for files in the root directory
                    res = BIDSValidator().is_bids(file)
            
                else:
                    # Modify file path to be relative to the root directory
                    relative_path = os.path.relpath(file_path, root_directory)
                    print(relative_path)
                    res = BIDSValidator().is_bids('/'+relative_path)
                    print(res)
                
                file_paths.append(res)  
        
        if all(file_paths):
            validate = 1
            print(f'BIDS data is valid for subject {subject_id} and session {session_id}')
        else:
            validate = 0
            print(f'BIDS data is invalid for subject {subject_id} and session {session_id}')
        return validate
    
# Convert the XDF file to BIDS

def bids_process_and_upload(processed_files, bids_root, project_root, project_name, project_stim_root):
    

    # argparser = argparse.ArgumentParser(description='Get the project name')
    # argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
    
    # project_name = argparser.parse_args().project_name
    # processed_files_file_path = 'processed_files.txt'


    # # Retrieve the list of processed files from processed_files.txt
    # processed_files = []
    # with open(processed_files_file_path, 'r') as f:
    #     for line in f:
    #         processed_files.append(line.strip())

    # Get the contents of the dataverse_config.yaml file
    with open("dataverse_config.yaml", "r") as yaml_file:
        data = yaml.safe_load(yaml_file)
        BASE_URL = data["BASE_URL"]
        API_TOKEN = data["API_TOKEN"]
        NAME = data["PARENT_DATAVERSE_NAME"]


    bids = BIDS()
    for file in processed_files:
        subject_id = file.split('_')[0]
        session_id = file.split('_')[1]
        filename = file.split(os.path.sep)[-1]
        project_path = os.path.join(project_root,project_name)
        xdf_path = os.path.join(project_path, subject_id, session_id, 'eeg',filename)
        toml_path = os.path.join(project_root,project_name,project_name+'_config.toml')

        with open(toml_path, 'r') as file:
            data = toml.load(file)
            stim = data["Computers"]["stimulusComputerUsed"]     
        
        val = bids.convert_to_bids(xdf_path,subject_id,session_id,bids_root,project_name,project_stim_root,stim)

        if val==1:
                            
                print('Generating metadatafiles........')   
                generate_json_file(project_root, project_name)
                print('Generating dataverse dataset........')
                
                doi, status = create_dataverse(BASE_URL, API_TOKEN, NAME, project_path,project_root,project_name)

                create_and_add_files_to_dataset(bids_root+project_name,status)

                user_input = input("Do you want to upload the files to Dataverse? (y/n): ")

                if user_input.lower() == "y":
                    print('Uploading to dataverse........')

                    print('Linking dataverse dataset with datalad')
                    add_sibling_dataverse_in_folder(bids_root+project_name,BASE_URL,doi,API_TOKEN)

                    print('Pushing files to dataverse........')
                    # Push the files to dataverse
                    push_files_to_dataverse(); 

                elif user_input.lower() == "n":
                    print("Program aborted.")
                else:
                    print("Invalid Input.")
        else:
            print("Program is aborted as all BIDS files are not validated")
            file = os.path.join(project_path,"last_run_log.txt")
            with open(file, 'w') as file:
                file.truncate(0)
            sys.exit()


