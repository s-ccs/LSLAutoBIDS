# Generate a default toml file in the dada/projects/<project_name> folder with id, project title properties
import yaml
import argparse

argparser = argparse.ArgumentParser(description='Get the project name')
argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
args = argparser.parse_args()
project_name = args.project_name


data = {
    "dataset_id": '123',
    "pid": '123',
    "project_title": 'default project title',
}

yaml_filename = 'data/projects/'+project_name+'/dataset_data.yaml'

# Write the data to the YAML file
with open(yaml_filename, "w") as yaml_file:
    yaml.dump(data, yaml_file, default_style='"')