import json
import toml
import os
import yaml


def read_toml_file(toml_file):
    with open(toml_file, 'r') as file:
        return toml.load(file)
    

def parse_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

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

def generate_json_file(project_root, project_name):
    # Load data from dataset.json
    with open(os.path.join(project_root, project_name, 'dataset.json'), 'r') as json_file:
        json_data = json.load(json_file)
    
    # Load data from projects.toml
    toml_data = read_toml_file(os.path.join(project_root, project_name, 'project.toml'))

    # Update the JSON data with values from the TOML file
    updated_json_data = update_json_data(json_data, toml_data)

    # Save the updated JSON data back to dataset.json
    with open(os.path.join(project_root, project_name, 'dataset.json'), 'w') as json_file:
        json.dump(updated_json_data, json_file, indent=4)

    print("Generated dataset.json file.")


