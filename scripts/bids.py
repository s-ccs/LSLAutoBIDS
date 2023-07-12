from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath
import os
from . import PROJECT_NAME,BIDS_ROOT


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
        
        os.symlink(xdf_file, dest_file) 
        
        
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

        # Validate the BIDS data
        self.validate_bids(BIDS_ROOT+PROJECT_NAME,subject_id,session_id)
    
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
            validate = 0
            print(f'BIDS data is invalid for subject {subject_id} and session {session_id}')
        return validate
