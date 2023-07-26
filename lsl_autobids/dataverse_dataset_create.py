# Dataverse Dataset creation
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file
import json
#import lsl_autobids.link_datalad_dataverse as link_datalad_dataverse

# get the url from darus_config.json from the root folder

with open('darus_config.json') as f:
    config = json.load(f)
    BASE_URL = config['BASE_URL']
    API_TOKEN = config['API_TOKEN']

ds_filename = 'dataset.json'
# Create the api object
api = NativeApi(BASE_URL, API_TOKEN)
ds = Dataset()
ds.from_json(read_file(ds_filename))

# Check thr validity of the json file
print('Checking the validity if the json file....')
print(ds.validate_json())

# Get the metadata for the parent dataverse
resp = api.get_dataverse("simtech_pn7_computational_cognitive_science")
print(resp.json()["data"])


# Create new Dataset
resp = api.create_dataset("simtech_pn7_computational_cognitive_science", ds.json())
#print(resp.json())
#ds_pid = resp.json()
#print(f"Dataset created with pid: {ds_pid}")

# Publish Dataset if you want to publish it
#resp = api.publish_dataset(ds_pid, release_type="major")


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

#ask_for_data_upload()