#import libraries
import os
import shutil
import logging
import sys
from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath

from generate_dataset_json import generate_json_file
from dataverse_dataset_create import create_dataverse
from datalad_create import create_and_add_files_to_datalad_dataset
from link_datalad_dataverse import add_sibling_dataverse_in_folder
from upload_to_dataverse import push_files_to_dataverse
from globals import project_root,project_stim_root, bids_root
from utils import get_user_input, read_toml_file

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class BIDS:
    """
    Class to handle conversion of EEG .xdf files to BIDS format and associated operations.
    """
    def __init__(self):
        pass


    def get_the_streams(self, xdf_path):
        """Retrieve stream names and information from an XDF file.

        Args:
            xdf_path (str): Path to the XDF file.

        Returns:
            tuple: List of stream names and stream info dictionaries.
        """
        streams = resolve_streams(xdf_path)
        
        stream_names = [streams[i]['name'] for i in range(len(streams))]
        return stream_names,streams


    def copy_source_files_to_bids(self,xdf_file,subject_id,session_id,project_name,stim):
        
        """
        Copy raw .xdf and optionally stimulus data to BIDS folder.

        Args:
            xdf_file (str): Full path to the .xdf file.
            subject_id (str): Subject identifier.
            session_id (str): Session identifier.
            project_name (str): Name of the project.
            stim (bool): Whether to copy stimulus/behavioral files as well.
        """
        ### COPY THE SOURCE FILES TO BIDS (recorded xdf file) ###
        
        # Get the source file name without the extension
        file_name = xdf_file.split(os.path.sep)[-1]
        file_name_without_ext, ext = os.path.splitext(file_name)
    
        # Copy the raw file
        new_filename = file_name_without_ext + '_raw' + ext
        
        # Destination path for the raw file
        dest_dir = os.path.join(bids_root , project_name , 'sourcedata' , subject_id , session_id , 'eeg')

        #check if the directory exists
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, new_filename)
        
        
        if os.path.exists(dest_file):
            logger.info("Raw XDF already exists in sourcedata.")
            pass
        else:
            shutil.copy(xdf_file, dest_file)
            logger.info(f"Copied {xdf_file} to {dest_file}")

      
        if stim:
            ### COPY THE BEHAVIOURAL FILES TO BIDS ###
            self._copy_behavioral_files(file_name_without_ext, project_name, subject_id, session_id)

            ### COPY THE EXPERIMENT FILES TO BIDS ###
            self._copy_experiment_files(project_name, subject_id, session_id)
        else:
            logger.info("Skipping copying of behavioral files and experiment files.")
        


    def _copy_behavioral_files(self, file_base, project_name, subject_id, session_id):
        """
        Copy behavioral files to the BIDS structure.

        Args:
            file_base (str): Base name of the file (without extension).
            project_name (str): Project name.
            subject_id (str): Subject ID.
            session_id (str): Session ID.
        """
        logger.info("Copying the behavioral files to BIDS...")
        # get the source path
        behavioural_path = os.path.join(project_stim_root,project_name,'data', subject_id,session_id,'beh')
        # get the destination path
        dest_dir = os.path.join(bids_root , project_name,  subject_id , session_id , 'beh')
        #check if the directory exists
        os.makedirs(dest_dir, exist_ok=True)
    
        for file in os.listdir(behavioural_path):
            # remove the _eeg from the file_name_without_ext
            file_name_without_eeg = file_base[:-4]
            new_filename = file_name_without_eeg + '_' + file
            dest_file = os.path.join(dest_dir, new_filename)
            if os.path.exists(dest_file):
                logger.info(f"Behavioural file {file} already exists in BIDS.")
                pass
            else:
                # Directly copy the file
                logger.info(f"Copying {file} to {dest_file}")
                shutil.copy(os.path.join(behavioural_path, file), dest_file)

    def _copy_experiment_files(self, file_base, project_name, subject_id, session_id):
        logger.info("Copying the experiment files to BIDS...")
    
        zip_file_path = os.path.join(bids_root, project_name,subject_id,session_id,"misc", 'experiment.zip')

        if os.path.exists(zip_file_path):
            logger.info("Experiment zip already exists. Skipping.")
            return
        # get the source path
        experiments_path = os.path.join(project_stim_root,project_name,'experiment')
        # get the destination path
        dest_dir = os.path.join(bids_root , project_name, subject_id,session_id, "misc",'experiment')
            
        #check if the directory exists
        os.makedirs(dest_dir, exists_ok =True)

        for file in os.listdir(experiments_path):
            src_file = os.path.join(experiments_path, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy(src_file, dest_file)

        # Compress the 'other' directory into a ZIP file
        shutil.make_archive(dest_dir, 'zip', dest_dir)

        #Remove the original 'other' directory
        shutil.rmtree(dest_dir)
        logger.info(f"Copied experiment files to {dest_dir} and zipped them.")

    def create_raw_xdf(self, xdf_path,streams):
        """
        Read XDF and convert to MNE Raw object.

        Args:
            xdf_path (str): Path to the .xdf file.
            streams (list): List of stream metadata.

        Returns:
            mne.io.Raw: Raw object ready for BIDS conversion.
        """
        # Get the stream id of the EEG stream
        stream_id = match_streaminfos(streams, [{"type": "EEG"}])[0]
        fs_new = max([stream["nominal_srate"] for stream in streams])
        logger.info("Reading xdf and resampling... let's hope the RAM is big enough")
        raw = read_raw_xdf(xdf_path,stream_ids=[stream_id],fs_new=fs_new,prefix_markers=True)
        logger.info("Resampling done! phew")
        # for memory reasons
        raw.resample(500)
        try:
            channelList = {'heog_u':'eog',
                                'heog_d':'eog',
                                'veog_r':'eog',
                                'veog_l':'eog',
                                'bipoc':'misc',
                                'VEOGD':'eog',
                                'VEOGU':'eog',
                                'HEOGL':'eog',
                                'HEOGR':'eog',
                                'sampleNumber':'misc'}
            raw.set_channel_types({k:channelList[k] for k in channelList.keys() if k in raw.ch_names})
        except ValueError as inst:
            logger.error(f"Error renaming channels: {inst}")
            logger.info(f"Available channel names: {raw.ch_names}")

        return raw

    def convert_to_bids(self, xdf_path,subject_id,session_id,project_name,stim):

        """
        Convert an XDF file to BIDS format.

        Args:
            xdf_path (str): Path to the .xdf file.
            subject_id (str): Subject identifier.
            session_id (str): Session identifier.
            project_name (str): Project name.
            stim (bool): Whether to copy stimulus/behavioral files as well.

        Returns:
            int: 1 if conversion is successful, 2 if the file already exists, 0 if validation fails.
        """
        logger.info("Converting to BIDS...")

        # Copy the experiment, behavioural and raw recorded files to BIDS
        self.copy_source_files_to_bids(xdf_path,subject_id,session_id, project_name,stim)

        # Get the bidspath for the raw file
        bids_path = BIDSPath(subject=subject_id[-3:], 
                            session=session_id[-3:], 
                            run=None, task=project_name, 
                            root=bids_root+project_name, 
                            datatype='eeg', 
                            suffix='eeg', 
                            extension='.set')
    
        if os.path.exists(bids_path):
            logger.info("BIDS file already exists. Skipping conversion.")
            return 2
        
        # Create the new raw file from xdf file
        _,streams = self.get_the_streams(xdf_path)
        raw = self.create_raw_xdf(xdf_path,streams)

        
        # Write the raw data to BIDS in EDF format
        # BrainVision format weird memory issues
        logger.log("Writing EEG-SET file")
        write_raw_bids(raw, bids_path, overwrite=False, verbose=False,symlink=False, format= "EEGLAB",allow_preload=True)

        logger.info("Conversion to BIDS complete.")
        # Validate BIDS data
        logger.info("Validating BIDS data...")
        # Validate the BIDS data
        val = self.validate_bids(bids_root+project_name,subject_id,session_id)
        return val
    
    def validate_bids(self,bids_path,subject_id,session_id):
        """
        Validate the BIDS format for all files in the BIDS path.

        Args:
            bids_path (str): Path to the BIDS directory.
            subject_id (str): Subject identifier.
            session_id (str): Session identifier.

        Returns:
            int: 1 if all files are valid, 0 if validation fails.
        """
        file_paths = []
        root_directory = os.path.abspath(bids_path)
        
        for root, _, files in os.walk(root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip non-relevant files
                if file_path.endswith(".xdf") or file_path.endswith(".zip") or 'beh' in file_path or file.startswith('.') or '.git' in file_path or os.path.basename(root).startswith('.'):
                    continue

                if root == root_directory:
                    # Validate BIDS for files in the root directory
                    res = BIDSValidator().is_bids(file)           
                else:
                    # Modify file path to be relative to the root directory
                    relative_path = os.path.relpath(file_path, root_directory)
                    res = BIDSValidator().is_bids('/'+relative_path)
    
                if not res:
                    print(f"Validation failed for {file_path}")
        
                
                file_paths.append(res)  
        
        if all(file_paths):
            logger.info(f"BIDS data is valid for subject {subject_id} and session {session_id}")
            return 1
        else:
            logger.error(f"BIDS data is invalid for subject {subject_id} and session {session_id}")
            return 0
    


def bids_process_and_upload(processed_files,project_name):
    """
    Process and upload BIDS files to Dataverse.
    Args:
        processed_files (list): List of processed files.
        project_name (str): Name of the project.
    """
    toml_path = os.path.join(project_root,project_name,project_name +'_config.toml')

    data = read_toml_file(toml_path)
    stim = data["Computers"]["stimulusComputerUsed"]     


    project_path = os.path.join(project_root,project_name)
    
    # Initialize BIDS object
    bids = BIDS()
    for file in processed_files:
        subject_id = file.split('_')[0]
        session_id = file.split('_')[1]
        filename = file.split(os.path.sep)[-1]
        logger.info(f"Currently processing {subject_id} / {session_id}")
        xdf_path = os.path.join(project_path, subject_id, session_id, 'eeg',filename)

        val = bids.convert_to_bids(xdf_path,subject_id,session_id,project_name,stim)

        if val == 1:
                logger.info("Bids Conversion Sucessful")      
        elif val == 2:
                logger.info("Converted file already found, skipping")   
        else:
            logger.error("Program is aborted as all BIDS files are not validated")
            file = os.path.join(project_path,"last_run_log.txt")
            with open(file, 'w') as file:
                file.truncate(0)
            sys.exit()
        
    logger.info("Conversion finished.")
    logger.info('Generating metadatafiles........')   
    generate_json_file(project_name)
    logger.info('Generating dataverse dataset........')
    
    doi, status = create_dataverse(project_name)
    
    logger.info("Creating and adding files to Dataverse dataset...")
    create_and_add_files_to_datalad_dataset(bids_root+project_name,status)
    
    if status == 0:
        logger.info('Linking dataverse dataset with datalad')
        add_sibling_dataverse_in_folder(doi)

    
    user_input = get_user_input("Do you want to upload the files to Dataverse? (y/n): ")

    if user_input.lower() == "y":
        logger.info('Pushing files to dataverse........')
        # Push the files to dataverse
        push_files_to_dataverse(project_name); 

    elif user_input.lower() == "n":
        logger.info("Program aborted.")
    else:
        logger.error("Invalid Input.")


