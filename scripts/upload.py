# Dataverse Dataset creation
from pyDataverse.api import NativeApi
import json

# get the url from darus_config.json from the root folder

with open('darus_config.json') as f:
    config = json.load(f)
    BASE_URL = config['BASE_URL']
    API_TOKEN = config['API_TOKEN']

print(BASE_URL)
print(API_TOKEN)
# Create the api object
#api = NativeApi(BASE_URL, API_TOKEN)