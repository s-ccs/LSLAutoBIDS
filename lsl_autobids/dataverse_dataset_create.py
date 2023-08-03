# Dataverse Dataset creation
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
import json
#import lsl_autobids.link_datalad_dataverse as link_datalad_dataverse

def create_dataverse():
    # Get the darus configuration data
    with open('./lsl_autobids/darus_config.json') as f:
        config = json.load(f)
        BASE_URL = config['BASE_URL']
        API_TOKEN = config['API_TOKEN']

    ds_filename = './lsl_autobids/dataset.json'
    
    # get the title of the dataset from the json file
    with open(ds_filename) as f:
        ds_title = json.load(f)['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value']

    # TODO - check if a dataverse with the same name exists


    # Create the api object
    api = NativeApi(BASE_URL, API_TOKEN)
    ds = Dataset()
    ds.from_json(read_file(ds_filename))

    # Check the validity of the json file
    print('Checking the validity if the json file....')
    if ds.validate_json():
        print('The dataset json file is validated.')

    # Get the metadata for the parent dataverse
    resp = api.get_dataverse("simtech_pn7_computational_cognitive_science")
    print(resp.json()["data"])

    # with open("temp","w") as f:
    #     f.write(ds.json())
    # with open("temp", 'r') as f:
    #     ds2 = f.read()
    #     ds2 = json.loads(ds2)
    #     ds2 = json.dumps(ds2)

    # Create new Dataset

    resp = api.create_dataset("simtech_pn7_computational_cognitive_science", ds.json())
    ds_pid = resp.json()['data']['persistentId']
    print(f"Dataset created with pid: {ds_pid}")

    # Publish Dataset if you want to publish it
    #resp = api.publish_dataset(ds_pid, release_type="major")

    return ds_pid

def ask_for_data_upload():
    while True:
        response = input(" Do you want to upload any data file? Please type 'yes' or 'no': ").lower()
        
        if response == 'yes':
            try:
                link_datalad_dataverse.check()
                break  # Assuming the script has a main() function to execute the upload.
            except ImportError:
                print("Error: The dataverse_upload.py script is not found.")
                break
            except Exception as e:
                print(f"Error occurred during data upload: {e}")
                break
        elif response == 'no':
            print("Alright! If you need any further assistance, feel free to ask.")
            break
        else:
            print("Invalid response. Please type 'yes' if you want to upload a data file or 'no' if you don't.")


def main():
    get_doi = create_dataverse()
    return get_doi
    #ask_for_data_upload()

if __name__ == "__main__":
    main()