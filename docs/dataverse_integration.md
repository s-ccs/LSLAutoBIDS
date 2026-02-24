### Dataverse Integration

#### 1. Generating dataset JSON Metadata (`generate_dataset_json.py`)

This module generates the `dataset.json` file required for creating a dataset in Dataverse. The function performs the following steps:

1. Gathers metadata from the project configuration file (<project_name>_config.toml) such as title, authors, description, license, etc.
2. Constructs a JSON structure that conforms to the Dataverse dataset metadata schema. This includes fields like title, author list, description, keywords, license, etc.
3. Writes the constructed JSON to a file named `dataset.json` in the project directory. This file is then used when creating the dataset in Dataverse.

#### 2. Dataverse Dataset Creation (`dataverse_dataset_create.py`)
This module handles the creation of a new dataset in Dataverse using the `pyDataverse` library. The function performs the following steps:

1. Initialize `dataset.json` file path and read the JSON content. (See section)
2. Sets up a Dataverse API connection using the base URL and API key from the global configuration file (`autobids_config.yaml`). This dataset then loads the  `dataset.json` into the Dataset. This json metadata populates the dataset metadata in Dataverse (title, authors, description, etc.), where we will eventually upload our datalad compatible BIDS dataset.
3. The dataset JSON is validated using `ds.validate_json()`. If the validation passes only then we proceed to create the dataset in Dataverse using `dv.create_dataset()`.
4. The function also checks if that dataset already exists in Dataverse (based on title) to avoid duplicates. For example, one dataverse dataset can contain data from multiple participants/subjects and we usually create a single dataset for the entire project but run the conversion for each subject separately. So we check if a dataset with the same title already exists in Dataverse.
    - Get all the datasets (pids) in the specified parent dataverse using `api.get_dataverse(parent_dataverse_name)`.
    - Check if that the PID specified in the response matches the Dataverse PID specified in the project config file. If it does, we log a message and skip creation.
5. If no existing dataset is found, we create a new dataset using `api.create_dataset(parent_dataverse_name, ds.json())`. We then populate the returned dataset ID and DOI in the project configuration file (<project_name>_config.toml) for using in future runs.
6. This function returns the dataset DOI and status code ( 1= dataverse dataset exists, 0= new dataset created)

#### 3. Linking DataLad to Dataverse (`link_datalad_dataverse.py`)
This module links the local DataLad dataset to the remote Dataverse dataset as a sibling. The function performs the following steps:
1. It first checks if the Dataverse is already created in the previous runs or it is just created in the current run (flag==0). If flag==0, it proceeds to link the DataLad dataset to Dataverse.
2. It runs the command `datalad add-sibling-dataverse dataverse_base_url doi_id`. This command adds the Dataverse as a sibling to the local DataLad dataset, allowing for synchronization and data management between the two. For lslautobids, we currently only allow to deposit data to Dataverse. In future version, we shall also add user controlled options for adding other siblings like github, gitlab, OpenNeuro, AWS etc.

We chose Dataverse as it serves as both a repository and a data sharing platform, making it suitable for our needs. It also integrates well with DataLad and allows sharing datasets with collaborators or the public.

Dataverse also provides features like versioning, but only after we publish the dataset. In our case, we keep the dataset in draft mode until we are ready to publish it (i.e. until all the participants/subjects data is uploaded). So we use DataLad for version control during the development and conversion phase to assure complete provenance of the dataset.

#### 4. Upload to Dataverse (`upload_to_dataverse.py`)

This module handles the uploading of files from the local DataLad dataset to the remote Dataverse dataset. The function performs the following steps:
1. It runs the command `datalad push --to dataverse` to push the files from the local DataLad dataset to the linked Dataverse dataset. This command uploads all changes (new files, modified files) to Dataverse.
2. If the `--yes` flag is set (in `lslautobids run`), it automatically pushes the files without user confirmation. Otherwise, it prompts the user for confirmation before proceeding with the upload.