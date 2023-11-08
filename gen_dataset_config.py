# Generate a default toml file in the dada/projects/<project_name> folder with id, project title properties
import yaml
import argparse

def parse_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

argparser = argparse.ArgumentParser(description='Get the project name')
argparser.add_argument('-p','--project_name', type=str, help='Enter the project name')
args = argparser.parse_args()
project_name = args.project_name


data = {
    "dataset_id": '123',
    "pid": '123',
    "project_title": 'default project title',
}

config_file = 'data_config.yaml'
config = parse_yaml_file(config_file)
project_root = config['PROJECT_ROOT']
yaml_filename = project_root +project_name+'/dataset_data.yaml'

# Write the data to the YAML file
with open(yaml_filename, "w") as yaml_file:
    yaml.dump(data, yaml_file, default_style='"')