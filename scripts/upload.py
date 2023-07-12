from config import load_config

config_file = "darus_config.json"
config = load_config(config_file)

# DaRUS credentials
API_URL = config["api_url"]
API_TOKEN = config["api_token"]
DOI_ID = config["doi_id"]


def upload_to_darus(file_path):
    """
    Uploads a file to Dataverse using the Dataverse API.
    
    Parameters:
        api_url (str): The base URL of the Dataverse API.
        api_token (str): The API token for authentication.
        dataset_id (str): The ID of the dataset in which to upload the file.
        file_path (str): The path to the file to upload.
    """
    url = f"{API_URL}/api/datasets/{DOI_ID}/add"
    headers = {"Content-Type": "application/json", "X-Dataverse-key": API_TOKEN}
    
    with open(file_path, "rb") as file:
        response = requests.post(url, headers=headers, files={"file": file})
        
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print(f"Failed to upload file. Status code: {response.status_code}")
    return 0
