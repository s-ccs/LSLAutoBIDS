import os
import yaml

class CLIArgs:
    _instance = None

    def __init__(self):
        self._args = None
        self._defaults = {
            "project_name": "default_project",
            "yes": False,
            "redo_bids_conversion": False,
            "reupload": False,
            "redo_stim_pc": False,
        }

    def init(self, args):
        self._args = args

    def __getattr__(self, name):
        if self._args and hasattr(self._args, name):
            return getattr(self._args, name)
        elif name in self._defaults:
            return self._defaults[name]
        else:
            raise AttributeError(f"'CLIArgs' has no attribute '{name}'")

# Singleton instance
cli_args = CLIArgs()


def parse_yaml_file(yaml_file):
    """
    Parse a YAML file and return the data

    Parameters
    ----------
    yaml_file : str
        Path to the root config YAML file

    Returns
    -------
    dict
        Data from the YAML file
    """
    with open(yaml_file, 'r') as file:
        try:
            data = yaml.safe_load(file)
            return data
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None


config_file = os.path.join(os.path.expanduser("~"),'.config/lslautobids/autobids_config.yaml')
config = parse_yaml_file(config_file)

project_root = os.path.join(os.path.expanduser("~"),config['PROJECT_ROOT'])
bids_root = os.path.join(os.path.expanduser("~"),config['BIDS_ROOT'])
project_stim_root = os.path.join(os.path.expanduser("~"),config['PROJECT_STIM_ROOT'])
api_key = config['API_KEY']
dataverse_base_url = config['BASE_URL']
parent_dataverse_name = config['PARENT_DATAVERSE_NAME']

