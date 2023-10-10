from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath
import os
import json
from folder_config import BIDS_ROOT,PROJECTS_STIM_ROOT
from main import PROJECT_NAME
# from generate_dataset_json import main as generate_dataset_json
# from dataverse_dataset_create import main as dataverse_dataset_create
# from datalad_create import main as datalad_create
# from link_datalad_dataverse import add_sibling_dataverse_in_folder

with open('darus_config.json') as f:
    config = json.load(f)
    BASE_URL = config['BASE_URL']
    NAME = config['NAME']

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


    def copy_source_files_to_bids(self,xdf_file,subject_id,session_id):

        # Get the file name without the extension
        file_name = xdf_file.split('/')[-1]
        file_name_without_ext, ext = os.path.splitext(file_name)
        
        # Copy the raw file
        new_filename = file_name_without_ext + '_raw' + ext
        
        # Destination path for the raw file
        dest_dir = BIDS_ROOT + PROJECT_NAME+ '/sourcedata/' + subject_id + '/' + session_id + '/eeg'

        #check if the directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, new_filename)
        
        # Create a symbolic link with the new filename pointing to the source file
        try:
            os.symlink(xdf_file, dest_file) 
        except FileExistsError:
            pass


        # Copy the behavioral file 
        
        behavioural_path = os.path.join(PROJECTS_STIM_ROOT,PROJECT_NAME,subject_id)
        # get the destination path
        dest_dir = BIDS_ROOT + PROJECT_NAME+ '/' + subject_id +'/'+ session_id + '/beh'
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
        
        # Copy the experiments file

        experiments_path = os.path.join(PROJECTS_STIM_ROOT,PROJECT_NAME,'experiment')
        # get the destination path
        dest_dir = BIDS_ROOT + PROJECT_NAME+ '/' + subject_id +'/'+ session_id + '/other'
        #check if the directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    
        for file in os.listdir(experiments_path):
            # remove the _eeg from the file_name_without_ext
            file_name_without_eeg = file_name_without_ext[:-4]
            new_filename = file_name_without_eeg + '_' + file
            dest_file = os.path.join(dest_dir, new_filename)
            try:
                # Create a symbolic link with the new filename pointing to the source file
                os.symlink(os.path.join(experiments_path,file), dest_file)
            except FileExistsError:
                pass


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

    def convert_to_bids(self, xdf_file,subject_id,session_id):
        
        print("Converting to BIDS........") 

        self.copy_source_files_to_bids(xdf_file,subject_id,session_id)
        
        print("Converting to BIDS........")

        # Create a copy of the raw xdf file in the BIDS structure
        file_name = xdf_file.split('/')[-1]
        file_name_without_ext, ext = os.path.splitext(file_name)
        new_filename = file_name_without_ext + '_raw' + ext
        
        # Destination path for the raw file
        dest_dir = BIDS_ROOT + PROJECT_NAME+ '/' + subject_id + '/' + session_id + '/eeg'

        #check if the directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, new_filename)

        # Create a symbolic link with the new filename pointing to the source file
        try:
            os.symlink(xdf_file, dest_file) 
        except FileExistsError:
            pass
        
        # Create the new raw file from xdf file
        _,streams = self.get_the_streams(xdf_file)
        raw = self.create_raw_xdf(xdf_file,streams)

        # Get the bidspath for the raw file
        bids_path = BIDSPath(subject=subject_id[-3:], 
                            session=session_id[-3:], 
                            run=None, task=PROJECT_NAME, 
                            root=BIDS_ROOT+PROJECT_NAME, 
                            datatype='eeg', 
                            suffix='eeg', 
                            extension='.vhdr')
        
        # Write the raw data to BIDS in BrainVision format
        write_raw_bids(raw, bids_path, overwrite=True, verbose=True,format='BrainVision',allow_preload=True)

        # # Validate the BIDS data
        # val = self.validate_bids(BIDS_ROOT+PROJECT_NAME,subject_id,session_id)
        # if val==1:
        #     # Generate the metadata json file
        #     generate_dataset_json()
        #     # generate dataverse dataset
        #     doi = dataverse_dataset_create()
        #     # datalad dataset create
        #     datalad_create()
        #     # link datalad to dataverse and upload to Darus
        #     add_sibling_dataverse_in_folder(BIDS_ROOT,BASE_URL,doi)
        # else:
        #     print('Upload to DaRUS failed as the BIDS format is invalid.')
    
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
            validate = 1
            print(f'BIDS data is valid for subject {subject_id} and session {session_id}')
        else:
            # TODO Change the validate value after we change the BIDS file structure
            validate = 1
            print(f'BIDS data is invalid for subject {subject_id} and session {session_id}')
        return validate
