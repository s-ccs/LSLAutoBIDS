# Dataverse Dataset creation
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
import toml
import json
import tomllib



def create_dataverse(BASE_URL, API_TOKEN, NAME,project_path,project_root,project_name):
    ds_filename = project_root + "/" + project_name + "/" +'dataset.json'
    flag=0
    
    # get the title of the dataset from the json file
    with open(ds_filename) as f:
        ds_title = json.load(f)['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value']


    # Create the api object
    api = NativeApi(BASE_URL, API_TOKEN)
    ds = Dataset()
    ds.from_json(read_file(ds_filename))

    # Check the validity of the json file
    print('Checking the validity if the json file....')
    if ds.validate_json():
        print('The dataset json file is validated.')

    # Get the metadata for the parent dataverse
    resp = api.get_dataverse(NAME)
    print(resp.json()["data"])

    # Get all the children
    resp1 = api.get_children(NAME,'dataverse',['datasets'])
    pids_resp1 = [id['pid'] for id in resp1]

    # open the toml file to get the dataset_id
    toml_path = project_root + "/" + project_name + "/" + "project.toml"
    with open(toml_path, 'rb') as file:
        data = tomllib.load(file)
        pid = data['Dataverse']['pid']

        if pid in pids_resp1:
            flag=1
            print('Dataset already exists.')
            return pid,flag
        else:
            print('Creating the dataset........')
            resp = api.create_dataset(NAME, ds.json())
            print(resp.json()['data'])
            ds_pid = resp.json()['data']['persistentId']
            dataset_id = resp.json()['data']['id']
            print(f"Dataset created with pid: {ds_pid}")


            # Modify field
            data['Dataverse']['dataset_title']=ds_title 
            data['Dataverse']['pid']=ds_pid
            data['Dataverse']['dataset_id']=dataset_id

            # To use the dump function, you need to open the file in 'write' mode
            # It did not work if I just specify file location like in load
            f = open(toml_path,'w')
            toml.dump(data, f)
            f.close()


            # # change the dataset_id in the yaml file
            # data['pid'] = ds_pid
            # data['dataset_id'] = dataset_id
            # data['dataset_title'] = ds_title

            # # write the updated yaml file
            # with open(project_path + '/dataset_data.yaml','w+') as yaml_file:
            #     yaml.dump(data,yaml_file)
            return ds_pid,flag
            





    # Publish Dataset if you want to publish it
    #resp = api.publish_dataset(ds_pid, release_type="major")

    #return ds_pid

# def ask_for_data_upload():
#     while True:
#         response = input(" Do you want to upload any data file? Please type 'yes' or 'no': ").lower()
        
#         if response == 'yes':
#             try:
#                 link_datalad_dataverse.check()
#                 break  # Assuming the script has a main() function to execute the upload.
#             except ImportError:
#                 print("Error: The dataverse_upload.py script is not found.")
#                 break
#             except Exception as e:
#                 print(f"Error occurred during data upload: {e}")
#                 break
#         elif response == 'no':
#             print("Alright! If you need any further assistance, feel free to ask.")
#             break
#         else:
#             print("Invalid response. Please type 'yes' if you want to upload a data file or 'no' if you don't.")
