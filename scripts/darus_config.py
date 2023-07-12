import json

def load_config(config_file):
    """
    Loads the configuration file and returns the credentials.
    
    Parameters:
        config_file (str): The path to the configuration file.
    
    Returns:
        dict: A dictionary containing the credentials.
    """
    with open(config_file, "r") as file:
        config = json.load(file)
    return config
