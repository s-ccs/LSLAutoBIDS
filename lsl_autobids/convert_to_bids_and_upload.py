#import libraries
from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
from bids_validator import BIDSValidator
from mne_bids import write_raw_bids, BIDSPath
import os
import shutil
from generate_dataset_json import generate_json_file
from dataverse_dataset_create import create_dataverse
from datalad_create import create_and_add_files_to_datalad_dataset
from link_datalad_dataverse import add_sibling_dataverse_in_folder
from upload_to_dataverse import push_files_to_dataverse
from globals import project_root,project_stim_root, bids_root
import toml
import yaml
import sys
import mne


class BIDS:
    def __init__(self):
        pass


    def get_the_streams(self, xdf_path):
        """
        Retrieve the stream names and information from an XDF file.

        Parameters:
        ----------
        xdf_path (str)
            The path to the XDF file

        Returns:
        tuple: A tuple containing the stream names and the stream information.

        """ 
        
        streams = resolve_streams(xdf_path)
        
        stream_names = [streams[i]['name'] for i in range(len(streams))]
        return stream_names,streams


    def copy_source_files_to_bids(self,xdf_file,subject_id,session_id,project_name,stim):
        
        """
        Copy the source files to the BIDS directory.

        Parameters:
        ----------
        xdf_file (str): The path to the XDF file.
        subject_id (str): The subject ID.
        session_id (str): The session ID.
        project_name (str): The project name.
        stim (bool): The stimulus computer used for the project.
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
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        dest_file = os.path.join(dest_dir, new_filename)
        
        
        if os.path.exists(dest_file):
            print("xdf already in sourcedata - not copying again")
            pass
        else:
            shutil.copy(xdf_file, dest_file)

        
        if stim:
            ### COPY THE BEHAVIOURAL FILES TO BIDS ###
            print('Copying the behavioural files to BIDS........')
        
            # get the source path
            behavioural_path = os.path.join(project_stim_root,project_name,'data', subject_id,session_id,'beh')
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
                if os.path.exists(dest_file):
                    print("...already exists")
                    pass
                else:
                    # Directly copy the file
                     #print(f"copying {behavioural_path}{file} to {dest_file}")
                     shutil.copy(os.path.join(behavioural_path, file), dest_file)
                    
            
            ### COPY THE EXPERIMENT FILES TO BIDS ###
            print('Copying the experiment files to BIDS........')
        
            zip_file_path = os.path.join(bids_root, project_name,subject_id,session_id,"misc", 'experiment.zip')

            if not os.path.exists(zip_file_path):
                experiments_path = os.path.join(project_stim_root,project_name,'experiment')
                # get the destination path
                dest_dir = os.path.join(bids_root , project_name, subject_id,session_id, "misc",'experiment')
                
                #check if the directory exists
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                for file in os.listdir(experiments_path):
                    src_file = os.path.join(experiments_path, file)
                    dest_file = os.path.join(dest_dir, file)
                    if os.path.isfile(src_file):
                        shutil.copy(src_file, dest_file)

                # Compress the 'other' directory into a ZIP file
                shutil.make_archive(dest_dir, 'zip', dest_dir)

                #Remove the original 'other' directory
                shutil.rmtree(dest_dir)
            else:
                print('Experiment zip files for the project already exist and hence not copied')

        else:
            print("STIM was set to false, not copying the behavioural and experiment files from a stimulus computer.")

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
        fs_new = max([stream["nominal_srate"] for stream in streams])
        print("reading xdf and resampling... if it breaks here, you need more RAM (close other programs, buy bigger RAM)")
        raw = read_raw_xdf(xdf_path,stream_ids=[stream_id],fs_new=fs_new,prefix_markers=True,interpolate_or_resample="interpolate")
        #print("interpolation done! phew")

        nan_annotations = mne.preprocessing.annotate_nan(raw)
        raw_annotations = raw.annotations
        bad_annotations = [idx for (idx,a) in enumerate(raw.annotations) if a['onset'] < 0]
        if len(bad_annotations)>0:
            print(f"Annotations: Deleted {len(bad_annotations)} annotations which started before time 0")
            print(raw_annotations[bad_annotations])
            raw_annotations.delete(bad_annotations)
        raw.set_annotations(raw_annotations+nan_annotations)



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
            print("error renaming channels, available channel names are:")
            print(raw.ch_names)
            print(inst)

        
        return raw

    def convert_to_bids(self, xdf_path,subject_id,session_id,project_name,stim):

        """
        Convert an XDF file to BIDS format.

        Parameters:
        ----------
        xdf_path (str): The path to the XDF file.
        subject_id (str): The subject ID.
        session_id (str): The session ID.
        project_name (str): The project name.
        stim (bool): The stimulus computer used for the project.

        """
        print("Converting to BIDS........") 

        # Copy the experiment and behavioural files to BIDS
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
            print("EEG target file already exists")
            return 2
        
        # Create the new raw file from xdf file
        _,streams = self.get_the_streams(xdf_path)
        raw = self.create_raw_xdf(xdf_path,streams)
        
        print("Writing EEG-SET file")

        write_raw_bids(raw, bids_path, overwrite=False, verbose=False,symlink=False, format= "EEGLAB",allow_preload=True)

        print("Conversion to BIDS complete.")

        print(' Validating the BIDS data........')
        # Validate the BIDS data
        val = self.validate_bids(bids_root+project_name,subject_id,session_id)
        return val
    
    def validate_bids(self,bids_path,subject_id,session_id):
        file_paths = []
        root_directory = os.path.abspath(bids_path)
        # print(root_directory)
        
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
                    if not res:
                        print(f"failed for {file}")
            
                else:
                    # Modify file path to be relative to the root directory
                    relative_path = os.path.relpath(file_path, root_directory)
                    # print(relative_path)
                    res = BIDSValidator().is_bids('/'+relative_path)
                    # print(res)
                    if not res:
                        print(f"failed for {file}")
                
                file_paths.append(res)  
        
        if all(file_paths):
            validate = 1
            print(f'BIDS data is valid for subject {subject_id} and session {session_id}')
        else:
            validate = 0
            print(f'BIDS data is invalid for subject {subject_id} and session {session_id}')
        return validate
    
# Convert the XDF file to BIDS

def bids_process_and_upload(processed_files,project_name):
    toml_path = os.path.join(project_root,project_name,project_name +'_config.toml')

    with open(toml_path, 'r') as file:
        data = toml.load(file)
        stim = data["Computers"]["stimulusComputerUsed"]     


    project_path = os.path.join(project_root,project_name)
    
    bids = BIDS()
    for file in processed_files:
        subject_id = file.split('_')[0]
        session_id = file.split('_')[1]
        filename = file.split(os.path.sep)[-1]
        print(f"Currently processing {subject_id} / {session_id}")
        xdf_path = os.path.join(project_path, subject_id, session_id, 'eeg',filename)

        val = bids.convert_to_bids(xdf_path,subject_id,session_id,project_name,stim)

        if val==1:
                print("bids conversion sucessfull")      
        elif val == 2:
                print("converted file already found, skipping")   
        else:
            print("Program is aborted as all BIDS files are not validated")
            file = os.path.join(project_path,"last_run_log.txt")
            with open(file, 'w') as file:
                file.truncate(0)
            sys.exit()
        
    print("Conversion finished.")
    print('Generating metadatafiles........')   
    generate_json_file(project_name)
    print('Generating dataverse dataset........')
    
    doi, status = create_dataverse(project_name)

    create_and_add_files_to_datalad_dataset(bids_root+project_name,status)
    
    if status == 0:
        print('Linking dataverse dataset with datalad')
        add_sibling_dataverse_in_folder(doi)

    
    user_input = input("Do you want to upload the files to Dataverse? (y/n): ")

    if user_input.lower() == "y":
        print('Pushing files to dataverse........')
        # Push the files to dataverse
        push_files_to_dataverse(project_name); 

    elif user_input.lower() == "n":
        print("Program aborted.")
    else:
        print("Invalid Input.")


