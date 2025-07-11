import json
import os
from lslautobids.config_globals import project_root
from lslautobids.utils import read_toml_file



def update_json_data(json_data, toml_data):
    # Update title field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value'] = toml_data['Dataset']['title']

    # Update author field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][1]['value'][0]['authorName']['value'] = toml_data['Authors']['authors']

    # Update dataset name and email field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactEmail']['value'] = toml_data['AuthorsContact']['email']
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][2]['value'][0]['datasetContactName']['value'] = toml_data['Authors']['authors']

    # Update dsDescription field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][3]['value'][0]['dsDescriptionValue']['value'] = toml_data['Dataset']['dataset_description']

    # Update subject field
    json_data['datasetVersion']['metadataBlocks']['citation']['fields'][4]['value'] = toml_data['Subject']['subject']
    return json_data

def generate_json_file(project_name, logger):
    json_file_path = os.path.join(project_root, project_name, 'dataset.json')

    try:
        # Try to load existing data from dataset.json
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
    except FileNotFoundError:
        logger.info(f"The 'dataset.json' file was not found. Creating a new one.")
        
        # Creating default data for the new dataset.json file
        default_data = {
            "datasetVersion": {
                "metadataBlocks": {
                    "citation": {
                        "fields": [
                            {
                                "typeName": "title",
                                "multiple": False,
                                "typeClass": "primitive",
                                "value": "Convert XDF to BIDS"
                            },
                            {
                                "typeName": "author",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "authorName": {
                                            "typeName": "author",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "Manpa Barman, Benedikt Ehinger"
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "datasetContact",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "datasetContactName": {
                                            "typeName": "datasetContactName",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "Manpa Barman, Benedikt Ehinger"
                                        },
                                        "datasetContactEmail": {
                                            "typeName": "datasetContactEmail",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "manpa.barman97@gmail.com"
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "dsDescription",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "dsDescriptionValue": {
                                            "typeName": "dsDescriptionValue",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "This is a test project to set up the pipeline to convert XDF to BIDS."
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "subject",
                                "multiple": True,
                                "typeClass": "controlledVocabulary",
                                "value": [
                                    "Medicine, Health and Life Sciences",
                                    "Engineering"
                                ]
                            }
                        ]
                    }
                }
            }
        }
        
        # Writing the default data to the new file
        with open(json_file_path, 'w') as new_json_file:
            json.dump(default_data, new_json_file, indent=4)
        
        # Assigning the default data to json_data
        json_data = default_data

    # Load data from projects.toml
    toml_data = read_toml_file(os.path.join(project_root, project_name, project_name+'_config.toml'))

    # Update the JSON data with values from the TOML file
    updated_json_data = update_json_data(json_data, toml_data)

    # Save the updated JSON data back to dataset.json
    with open(json_file_path, 'w') as json_file:
        json.dump(updated_json_data, json_file, indent=4)

    logger.info("Generated dataset.json file.")
