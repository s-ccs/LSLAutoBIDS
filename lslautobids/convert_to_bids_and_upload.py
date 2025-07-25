#import libraries
import os
import shutil
import sys

from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath, get_anonymization_daysback,  make_dataset_description
import mne

from lslautobids.generate_dataset_json import generate_json_file
from lslautobids.dataverse_dataset_create import create_dataverse
from lslautobids.datalad_create import create_and_add_files_to_datalad_dataset
from lslautobids.link_datalad_dataverse import add_sibling_dataverse_in_folder
from lslautobids.upload_to_dataverse import push_files_to_dataverse
from lslautobids.config_globals import cli_args, project_root, bids_root, project_stim_root
from lslautobids.utils import get_user_input, read_toml_file
import json


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


    def copy_source_files_to_bids(self,xdf_file,subject_id,session_id,stim, logger):
        
        """
        Copy raw .xdf and optionally stimulus data to BIDS folder.

        Args:
            xdf_file (str): Full path to the .xdf file.
            subject_id (str): Subject identifier.
            session_id (str): Session identifier.
            stim (bool): Whether to copy stimulus/behavioral files as well.
        """
        ### COPY THE SOURCE FILES TO BIDS (recorded xdf file) ###
        project_name = cli_args.project_name
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
            self._copy_behavioral_files(file_name_without_ext,subject_id, session_id, logger)

            ### COPY THE EXPERIMENT FILES TO BIDS ###
            self._copy_experiment_files(subject_id, session_id, logger)
        else:
            logger.info("Skipping copying of behavioral files and experiment files.")
    


    def _copy_behavioral_files(self, file_base, subject_id, session_id, logger):
        """
        Copy behavioral files to the BIDS structure.

        Args:
            file_base (str): Base name of the file (without extension).
            subject_id (str): Subject ID.
            session_id (str): Session ID.
        """
        project_name = cli_args.project_name
        logger.info("Copying the behavioral files to BIDS...")
        # get the source path
        behavioural_path = os.path.join(project_stim_root,project_name,'data', subject_id,session_id,'beh')
        # get the destination path
        dest_dir = os.path.join(bids_root , project_name,  subject_id , session_id , 'beh')
        #check if the directory exists
        os.makedirs(dest_dir, exist_ok=True)

        processed_files = []
        # Extract the sub-xxx_ses-yyy part
        def extract_prefix(filename):
            parts = filename.split("_")
            sub = next((p for p in parts if p.startswith("sub-")), None)
            ses = next((p for p in parts if p.startswith("ses-")), None)
            if sub and ses:
                return f"{sub}_{ses}_"
            return None
        
        prefix = extract_prefix(file_base)

        for file in os.listdir(behavioural_path):
            # Skip non-files (like directories)
            original_path = os.path.join(behavioural_path, file)
            if not os.path.isfile(original_path):
                continue
            
            if not file.startswith(prefix):
                logger.info(f"Renaming {file} to include prefix {prefix}")
                renamed_file = prefix + file
            else:
                renamed_file = file
        
            processed_files.append(renamed_file)
            dest_file = os.path.join(dest_dir, renamed_file)
        
            if cli_args.redo_stim_pc:
                logger.info(f"Copying (overwriting if needed) {file} to {dest_file}")
                shutil.copy(original_path, dest_file)
            else:
                if os.path.exists(dest_file):
                    logger.info(f"Behavioural file {file} already exists in BIDS. Skipping.")
                else:
                    logger.info(f"Copying new file {file} to {dest_file}")
                    shutil.copy(original_path, dest_file)



        unnecessary_files = self._check_required_behavioral_files(processed_files, prefix, logger)

        # remove the unnecessary files
        for file in unnecessary_files:
            file_path = os.path.join(dest_dir, file)
            if os.path.exists(file_path):
                logger.info(f"Removing unnecessary file: {file_path}")
                os.remove(file_path)
            else:
                logger.warning(f"File to remove does not exist: {file_path}")


    
    def _check_required_behavioral_files(self, files, prefix, logger):
        """
        Check for required behavioral files after copying.

        Args:
            files (list): List of copied file names.
            prefix (str): Expected prefix (e.g., "sub-001_ses-002_").
        """
        logger.info("Checking for required behavioral files...")

        # Get the expected file names from the toml file
        toml_path = os.path.join(project_root, cli_args.project_name, cli_args.project_name + '_config.toml')
        data = read_toml_file(toml_path)

        required_files = data["ExpectedStimulusFiles"]["expectedFiles"]


        for required_file in required_files:
            if not any(f.startswith(prefix) and f.endswith(required_file) for f in files):
                raise FileNotFoundError(f"Missing required behavioral file: {required_file}")
        
        unnecessary_files = []
        # remove everything except the required files
        for file in files:
            if not any(file.endswith(required_file) for required_file in required_files):
                unnecessary_files.append(file)
        return unnecessary_files


    def _copy_experiment_files(self, subject_id, session_id, logger):
        """
        Copy experimental files

        Args:
        subject_id (str): Subject ID.
        session_id (str): Session ID.
        """
        project_name = cli_args.project_name
        logger.info("Copying the experiment files to BIDS...")
    
        zip_file_path = os.path.join(bids_root, project_name,subject_id,session_id,"misc", 'experiment.tar.gz')

        if os.path.exists(zip_file_path):
            logger.info("Experiment tar.gz already exists. Skipping.")
            if not cli_args.redo_stim_pc:
                logger.info("Skipping experiment file copy ")
                return
            else:
                logger.info("Overwriting existing experiment archive due to --redo_stim_pc flag.")
        

        # get the source path
        experiments_path = os.path.join(project_stim_root,project_name,'experiment')
        # get the destination path
        dest_dir = os.path.join(bids_root , project_name, subject_id,session_id, "misc",'experiment')
            
        #check if the directory exists
        os.makedirs(dest_dir, exist_ok =True)

        for file in os.listdir(experiments_path):
            src_file = os.path.join(experiments_path, file)
            dest_file = os.path.join(dest_dir, file)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_file)

        # Compress the 'other' directory into a ZIP file
        shutil.make_archive(dest_dir, 'gztar', dest_dir)

        #Remove the original 'other' directory
        shutil.rmtree(dest_dir)
        logger.info(f"Copied experiment files to {dest_dir} and zipped them.")
    


    def create_raw_xdf(self, xdf_path,streams, logger):
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

        logger.info("Reading xdf and resampling... if it breaks here, you need more RAM (close other programs, buy bigger RAM)")
        raw = read_raw_xdf(xdf_path,stream_ids=[stream_id],fs_new=fs_new,prefix_markers=True,interpolate_or_resample="interpolate")
        logger.info("Interpolation done! phew")

        nan_annotations = mne.preprocessing.annotate_nan(raw)
        raw_annotations = raw.annotations
        bad_annotations = [idx for (idx,a) in enumerate(raw.annotations) if a['onset'] < 0]
        if len(bad_annotations)>0:
            print(f"Annotations: Deleted {len(bad_annotations)} annotations which started before time 0")
            print(raw_annotations[bad_annotations])
            raw_annotations.delete(bad_annotations)
        raw.set_annotations(raw_annotations+nan_annotations)


        try:
            channelList = {     'heog':'eog',
                                'veog':'eog',
                                'veog_u':'eog',
                                'veog_d':'eog',
                                'veog_l':'eog',
                                'heog_r':'eog',
                                'heog_l':'eog',
                                'bipoc':'misc',
                                'VEOGD':'eog',
                                'VEOGL':'eog',
                                'VEOGU':'eog',
                                'HEOGL':'eog',
                                'HEOGR':'eog',
                                'sampleNumber':'misc'}
            raw.set_channel_types({k:channelList[k] for k in channelList.keys() if k in raw.ch_names})
        except ValueError as inst:
            logger.error(f"Error renaming channels: {inst}")
            logger.info(f"Available channel names: {raw.ch_names}")

        return raw

    def convert_to_bids(self, xdf_path,subject_id,session_id, run_id, task_id,stim, logger):

        """
        Convert an XDF file to BIDS format.

        Args:
            xdf_path (str): Path to the .xdf file.
            subject_id (str): Subject identifier.
            session_id (str): Session identifier.
            stim (bool): Whether to copy stimulus/behavioral files as well.

        Returns:
            int: 1 if conversion is successful, 2 if the file already exists, 0 if validation fails.
        """
        project_name = cli_args.project_name
        logger.info("Converting to BIDS...")

        # Copy the experiment, behavioural and raw recorded files to BIDS
        self.copy_source_files_to_bids(xdf_path,subject_id,session_id,stim, logger)

        # Get the bidspath for the raw file
        bids_path = BIDSPath(subject=subject_id[-3:], 
                            session=session_id[-3:], 
                            task=task_id, 
                            run=int(run_id[-3:]) ,
                            root=bids_root+project_name, 
                            datatype='eeg', 
                            suffix='eeg', 
                            extension='.set')
        
        # Force BIDS conversion
        if not cli_args.redo_bids_conversion:
            if os.path.exists(bids_path):
                logger.info("BIDS file already exists. Skipping conversion.")
                return 2
        else:
            logger.info("Forcing BIDS conversion, existing files will be overwritten.")
     
        
        # Create the new raw file from xdf file
        _,streams = self.get_the_streams(xdf_path)
        raw = self.create_raw_xdf(xdf_path,streams, logger)

        # Set up anonymization
        daysback_min, _ = get_anonymization_daysback(raw)

        # get the anonymization number from the toml file
        toml_path = os.path.join(project_root,project_name,project_name+'_config.toml')
        data = read_toml_file(toml_path)
        anonymization_number = data["Subject"]["anonymization_number"]

        # Write the raw data to BIDS in EDF format
        # BrainVision format weird memory issues
        logger.info("Writing EEG-SET file")
        write_raw_bids(raw, bids_path, overwrite=cli_args.redo_bids_conversion, verbose=False,symlink=False, format= "EEGLAB",allow_preload=True, anonymize = dict(daysback=daysback_min + anonymization_number,keep_his=True))


        logger.info("Conversion to BIDS complete.")
        # Validate BIDS data
        logger.info("Validating BIDS data...")
        # Validate the BIDS data
        val = self.validate_bids(bids_root+project_name,subject_id,session_id, logger)
        return val
    
    def validate_bids(self,bids_path,subject_id,session_id, logger):
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
                if file_path.endswith(".xdf") or file_path.endswith(".tar.gz") or 'beh' in file_path or file.startswith('.') or '.git' in file_path or os.path.basename(root).startswith('.'):
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

    def populate_dataset_description_json(self, project_name, logger):
        """
        Populate the dataset_description.json file with metadata from the project configuration.

        Args:
            project_name (str): Name of the project.
        """
        toml_path = os.path.join(project_root, project_name, project_name + '_config.toml')
        data = read_toml_file(toml_path)

        # open the dataset_description.json file
        dataset_description_path = os.path.join(bids_root, project_name)

        make_dataset_description(
            path = dataset_description_path,
            name = data["Dataset"]["title"],
            data_license = data["Dataset"]["License"],
            authors = data["Authors"]["authors"],
            overwrite= True, #necessary to overwrite the existing file created by mne_bids.write_raw_bids()
        )


        logger.info(f"dataset_description.json updated successfully for project '{project_name}'.")

def bids_process_and_upload(processed_files,logger):
    """
    Process and upload BIDS files to Dataverse.
    Args:
        processed_files (list): List of processed files.

    """

    project_name = cli_args.project_name
    toml_path = os.path.join(project_root,project_name,project_name +'_config.toml')

    data = read_toml_file(toml_path)
    stim = data["Computers"]["stimulusComputerUsed"]     

    project_path = os.path.join(project_root,project_name)
    logger.info("Initializing BIDS conversion and upload process...")
    # Initialize BIDS object
    bids = BIDS()
    for file in processed_files:
        subject_id = file.split('_')[0]
        session_id = file.split('_')[1]
        run_id = file.split('_')[3]
        task_id = file.split('_')[2].split('-')[1]
        filename = file.split(os.path.sep)[-1]
        logger.info(f"Currently processing {subject_id}, {session_id}, {run_id} of task : {task_id}") 
        xdf_path = os.path.join(project_path, subject_id, session_id, 'eeg',filename)

        val = bids.convert_to_bids(xdf_path,subject_id,session_id, run_id, task_id, stim, logger)   

        if val == 1:
                logger.info("BIDS Conversion Successful")      
        elif val == 2:
                logger.info("Converted file already found, skipping")   
        else:
            logger.error("Program is aborted as all BIDS files are not validated")
            file = os.path.join(project_path,"last_run_log.txt")
            with open(file, 'w') as file:
                file.truncate(0)
            sys.exit()
        
    logger.info("Conversion finished.")
    logger.info("Populating dataset_description.json file with metadata...")
    bids.populate_dataset_description_json(project_name, logger)
    logger.info('Generating metadatafiles........')   
    generate_json_file(project_name, logger)
    logger.info('Generating dataverse dataset........')
    
    doi, status = create_dataverse(project_name)
    
    logger.info("Creating and adding files to Dataverse dataset...")
    create_and_add_files_to_datalad_dataset(bids_root+project_name,status, logger)
    
    if status == 0:
        logger.info('Linking dataverse dataset with datalad')
        add_sibling_dataverse_in_folder(doi, logger)

    if cli_args.yes:
        logger.info('Pushing files to dataverse........')
        push_files_to_dataverse(project_name, logger)
    else:
        user_input = get_user_input("Do you want to push the files to Dataverse? ",logger)
        if user_input == "y":
            logger.info('Pushing files to dataverse........')
            push_files_to_dataverse(project_name, logger)
        elif user_input == "n":
            logger.info("Program aborted.")
        else:
            logger.error("Invalid Input.")
