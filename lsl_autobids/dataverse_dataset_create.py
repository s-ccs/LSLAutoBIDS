# Dataverse Dataset creation
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
import json 
import os
from config_globals import project_root, dataverse_base_url, api_key, parent_dataverse_name
import logging
from utils import read_toml_file, write_toml_file

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def create_dataverse(project_name):
    """
    Creates a Dataverse dataset and returns the PID and dataset ID.
    
    This function checks if the dataset already exists in the parent Dataverse.
    If it exists, it returns the existing PID. If not, it creates a new dataset
    and updates the TOML file with the new dataset PID and ID.
    
    Args:
        project_name (str): The name of the project.
        
    Returns:
        tuple: A tuple containing the dataset PID and a flag indicating whether 
               the dataset already exists (1 if it exists, 0 if created).
               
    Raises:
        Exception: If there is an error during the Dataverse dataset creation process.
    """
    ds_filename = os.path.join(project_root, project_name,'dataset.json')
    flag=0
    
    # get the title of the dataset from the json file
    with open(ds_filename) as f:
        ds_title = json.load(f)['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value']


    # Create the api object
    api = NativeApi(dataverse_base_url, api_key)
    ds = Dataset()
    ds.from_json(read_file(ds_filename))

    # Check the validity of the json file
    logger.info('Checking the validity of the JSON file...')
    if not ds.validate_json():
        logger.error('Invalid dataset JSON file.')
        raise ValueError('Invalid dataset JSON file.')
    logger.info('The dataset JSON file is valid.')

    # Get the metadata for the parent dataverse
    resp = api.get_dataverse(parent_dataverse_name)
    logger.info(f"Parent Dataverse Metadata: {resp.json()['data']}")

    # Get all the children
    resp1 = api.get_children(parent_dataverse_name,'dataverse',['datasets'])
    
    pids_resp1 = [id['pid'].lower() for id in resp1]

    # open the toml file to get the dataset_id
    toml_path = os.path.join(project_root,project_name,project_name+'_config.toml')
   
    data = read_toml_file(toml_path)
    pid = data['Dataverse']['pid']

    if pid.lower() in pids_resp1:
        flag=1
        logger.info('Dataset already exists.')
        return pid,flag
    else:
        logger.info('Creating the dataset........')
        resp = api.create_dataset(parent_dataverse_name, ds.json())
        logger.info(f"Dataset created with PID: {resp.json()['data']['persistentId']}")
   
        # Modify field
        data['Dataset']['title']=ds_title 
        data['Dataverse']['pid']= resp.json()['data']['persistentId']
        #data['Dataverse']['dataset_id']= resp.json()['data']['id']

        # To use the dump function, you need to open the file in 'write' mode
        # It did not work if I just specify file location like in load
        write_toml_file(toml_path,data)
        
        # # change the dataset_id in the yaml file
        # data['pid'] = ds_pid
        # data['dataset_id'] = dataset_id
        # data['dataset_title'] = ds_title

        # # write the updated yaml file
        # with open(project_path + '/dataset_data.yaml','w+') as yaml_file:
        #     yaml.dump(data,yaml_file)
        return resp.json()['data']['persistentId'],flag
        
