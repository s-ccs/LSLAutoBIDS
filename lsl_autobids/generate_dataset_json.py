import json
import toml
from .folder_config import PROJECT_NAME, PROJECT_ROOT
import os


def read_toml_file(toml_file):
    with open(toml_file, 'r') as file:
        return toml.load(file)

def update_json_data(json_data, toml_data):
    # Update title field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value'] = toml_data['Dataset']['title']

    # Update author field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][1]['value'][0]['authorName']['value'] = toml_data['Authors']['authors']

    # Update dataset name and email field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'] = toml_data['Authors']['authors']
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'] = toml_data['AuthorsContact']['email']
    # Update dsDescription field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'] = toml_data['Dataset']['dataset_description']

    # Update subject field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][4]['value'] = toml_data['Subject']['subject']
    return json_data

def main():

    # Load data from dataset.json
    with open('./lsl_autobids/dataset.json', 'r') as json_file:
        json_data = json.load(json_file)

    # Load data from projects.toml
    toml_data = read_toml_file(os.path.join(PROJECT_ROOT, PROJECT_NAME, 'project.toml'))

    # Update the JSON data with values from the TOML file
    updated_json_data = update_json_data(json_data, toml_data)

    # Save the updated JSON data back to dataset.json
    with open('./lsl_autobids/dataset.json', 'w') as json_file:
        json.dump(updated_json_data, json_file, indent=4)

if __name__ == "__main__":
    main()