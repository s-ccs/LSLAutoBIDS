 
# LSLAutoBIDS Developer's Documentation

## Overview

LSLAutoBIDS is a Python tool series designed to automate the following tasks sequentially:
- Convert recorded XDF files to BIDS format
- Integrate the EEG data with non-EEG data (e.g., behavioral, other) for the complete dataset 
- Datalad integration for version control for the integrated dataset
- Upload the dataset to Dataverse 
- Provide a command-line interface for cloning, configuring, and running the conversion process


### Key Features

- Automatic XDF to BIDS conversion
- DataLad integration for version control
- Dataverse integration for data sharing
- Configurable project management
- Support for behavioral data (non eeg files) in addition to EEG data
- Comprehensive logging and validation for BIDS compliance


## Table of Contents
- [Overview](#overview)
- [Core Components](#core-components)
  - [1. CLI Module (`cli.py`)](#1-cli-module-clipy)
  - [2. Configuration System](#2-configuration-system)
    - [1. Dataverse and Project Root Configuration (`gen_dv_config.py`)](#1-dataverse-and-project-root-configuration-gen_dv_configpy)
    - [2. Project Configuration (`gen_project_config.py`)](#2-project-configuration-gen_project_configpy)
  - [3. File Processing Pipeline (`processing_new_files.py`)](#3-file-processing-pipeline-processing_new_filespy)
    - [1. Detection of New Files (`check_for_new_data()`)](#1-detection-of-new-files-check_for_new_data)
    - [2. Filtering (`check_for_new_files()`)](#2-filtering-check_for_new_files)
    - [3. Validation and Preparation – (`process_new_files()`)](#3-validation-and-preparation--process_new_files)
    - [4. User Prompt & Conversion](#4-user-prompt--conversion)
    - [5. BIDS Conversion and Upload (`bids_process_and_upload()`)](#5-bids-conversion-and-upload-bids_process_and_upload)
    - [6. Supporting Utility](#6-supporting-utility)

  - [4. BIDS Conversion and Upload Pipeline ⚙️ (`convert_to_bids_and_upload.py`)](#4-bids-conversion-and-upload-pipeline-️-convert_to_bids_and_uploadpy)
    - [1. Entry Point (`bids_process_and_upload()`)](#1-entry-point-bids_process_and_upload)
    - [2. Convert to BIDS (`convert_to_bids()`)](#2-convert-to-bids-convert_to_bids)
    - [3. Copy Source Files (`copy_source_files_to_bids()`)](#3-copy-source-files-copy_source_files_to_bids)
    - [4. Create Raw XDF (`create_raw_xdf()`)](#4-create-raw-xdf-create_raw_xdf)
    - [5. BIDS Validation (`validate_bids()`)](#5-bids-validation-validate_bids)
    - [6. Populate dataset_description.json (`populate_dataset_description_json()`)](#6-populate-dataset_descriptionjson-populate_dataset_description_json)
    - [7. Datalad and Dataverse Integration](#7-datalad-and-dataverse-integration)
  - [5. DataLad Integration (`datalad_create.py`)](#4-datalad-integration-datalad_createpy)
  - [6. Dataverse Integration](#5-dataverse-integration)
    - [1. Dataverse Dataset Creation (`dataverse_dataset_create.py`)](#1-dataverse-dataset-creation-dataverse_dataset_createpy)
    - [2. Linking DataLad to Dataverse (`link_datalad_dataverse.py`)](#2-linking-datalad-to-dataverse-link_datalad_dataversepy)
    - [3. Generating dataset JSON Metadata (`generate_dataset_json.py`)](#4-generating-dataset-json-metadata-generate_dataset_jsonpy)
    - [4. Upload to Dataverse (`upload_to_dataverse.py`)](#5-upload-to-dataverse-upload_to_dataversepy)
  - [Other Utility Modules](#other-utility-modules)
    - [1. Global Configuration Management (`config_globals.py`)](#1-global-configuration-management-config_globalspy)
    - [2. Logging Configuration (`config_logger.py`)](#2-logging-configuration-config_loggerpy)
    - [3. Utility Functions (`utils.py`)](#3-utility-functions-utilspy)

- [Testing](#testing)
  - [Running Tests](#running-tests)


## Architecture - TODO

The system follows a modular architecture with clear separation of concerns:
<TODO: Add architecture diagram here>

## Core Components

### 1. CLI Module (`cli.py`)

The command-line interface provides the main entry point for the application:

- **Commands**: `gen-proj-config`, `run`, `gen-dv-config`, `help`
- **Module mapping**: Maps commands to their respective modules
- **Argument handling**: Processes and forwards command-line arguments

#### Key Points

1. `lslautobids en-proj-config` and `lslautobids gen-dv-config` commands generate configuration files for the project and Dataverse, respectively. This allows users to set up their project and Dataverse connection details easily before running the conversion and upload process
2. The `lslautobids run` command executes the main conversion and upload process, using the configurations generated earlier. This command runs the entire pipeline from reading XDF files, converting them to BIDS format, integrating with DataLad, and uploading to Dataverse.
3. The `lslautobids help` command provides usage information for the CLI, listing available commands and their descriptions.

### 2. Configuration System

The configuration system manages dataversse and project-specific settings using YAML and TOML files.

#### 1. Dataverse and Project Root Configuration (`gen_dv_config.py`)

This module generates a global configuration file for Dataverse and project root directories. This is a one-time setup per system.  This file is stored in `~/.config/lslautobids/autobids_config.yaml` and contains:
- Paths for BIDS, projects, and project_other directories : This allows users to specify where their eeg data, behavioral data, and converted BIDS data are stored on their system. This paths should be relative to the home/users directory of your system and string format.

- Dataverse connection details: Base URL, API key, and parent dataverse name for uploading datasets. Base URL is the URL of the dataverse server (e.g. https://darus.uni-stuttgart.de), API key is your personal API token for authentication (found in your dataverse account settings), and parent dataverse name is the name of the dataverse under which datasets will be created (this can be found in the URL when you are in the dataverses page just after 'dataverse/'). For example, if the URL is `https://darus.uni-stuttgart.de/dataverse/simtech_pn7_computational_cognitive_science`, then the parent dataverse name is `simtech_pn7_computational_cognitive_science`.

**Commands and arguments**

The command to generate the dataverse configuration file is:
```
lslautobids gen-dv-config
```
_Currently, the package doesn't allow you to have multiple dataverse configurations. This will be added in future versions and can be easily adapted_

However for testing purposes, we create a separate test configuration file `~/.config/lslautobids/test-autobids_config.yaml` which is used when running the tests.

#### 2. Project Configuration (`gen_project_config.py`)
This module generates a project-specific configuration file in TOML format. This file is stored in the `projects/<PROJECT_NAME>/<PROJECT_NAME>_config.toml` file and contains:
- Project metadata: Title, description, license, and authors, etc.
<Change the configuration file details as per new edits>


**Commands and arguments**

The command to generate the project configuration file is:
```
lslautobids gen-proj-config --project <projectname>  
```
- `--project <projectname>`: Specifies the name of the project for which the configuration file is to be generated. This argument is *required*.
- `--standalone_toml` : (Optional) If provided, the generated configuration file will be a standalone TOML file in the current directory, without being placed in the project directory.
- `--custom_dv_config` : (Optional) Path to a custom YAML configuration file (dataverse and project root configuration) for Dataverse and project root directories. If not provided, the default path `~/.config/lslautobids/autobids_config.yaml` will be used. This is specified to allow flexibility in using different configurations for different projects or testing purposes.


### 3. File Processing Pipeline (`processing_new_files.py`)

The file processing part of the pipeline handles finding and processing new XDF files in the specified project directory:

The pipeline ensures that all newly added data files are:

1. Detected since the last run.

2. Filtered based on ignored subjects and tasks (these are specified in the project configuration file).

3. Validated against duplicate or malformed filenames.

4. Registered in the project configuration file (e.g., tasks ,etc.).

5. Converted to BIDS format and uploaded, based on user confirmation or auto-run flags.

#### 1. Detection of New Files (`check_for_new_data()`)

- Entry point of the script (from `main.py`).

- Reads project configuration (<project_name>_config.toml) to identify ignored subjects and excluded tasks (which we don't want to process and include in the BIDS dataset).

- Calls `check_for_new_files()` to scan the project directory for files modified after the last recorded run.

#### 2. Filtering (`check_for_new_files()`)

- Uses `last_run_log.txt` to determine which files are new since the last check.

- Excludes:

    - Ignored subjects (defined in the project TOML config).

    - Ignored tasks (tasks explicitly excluded in the project TOML config).

- Returns a list of candidate `.xdf` files to process or outputs a message if no new files are found and exits.

#### 3. Validation and Preparation – (`process_new_files()`)

For each new file:

- File type check: Only .xdf files are considered.

- Duplicate prevention: Files with a _old suffix (e.g., sub-001_ses-01_task-Default_old.xdf) are flagged as duplicates. The pipeline logs an error and halts execution to avoid accidental overwrites. This is currently a specific duplicate check for LSL recordings. We shall extend this in future versions.

- Task extraction: Task names are parsed from filenames (e.g., sub-888_ses-001_task-Default_run-001_eeg.xdf → task = Default).

- Configuration update: Newly discovered tasks are appended to the TOML config under [Tasks.tasks].

#### 4. User Prompt & Conversion

- If cli_args.yes is set (as a flag while running `lslautobids run`), the pipeline skips user interaction and proceeds directly to conversion. In general, this flag sets all the user prompts throughout the pipeline to 'yes', allowing for fully automated runs. 
- Otherwise, the user is prompted to confirm whether BIDS conversion should start.

- If declined, the process halts with a warning.

#### 5. BIDS Conversion and Upload (`bids_process_and_upload()`)

- Invoked only if the user confirms (or auto-run flag is set).

- Handles BIDS formatting and uploading of the processed files.

#### 6. Supporting Utility

- `_clear_last_run_log()` :Clears the last run timestamp (last_run_log.txt) when --redo_bids_conversion is specified (as a flag in `lslautobids run`), forcing reprocessing of all files.


### 4. BIDS Conversion and Upload Pipeline ⚙️ (`convert_to_bids_and_upload.py`)

The pipeline is designed to ensure:

1. Source files (EEG only) are preserved in a BIDS-compatible structure.

2. EEG recordings are converted to BIDS format using MNE and validated against the BIDS standard.

3. Behavioral and experimental metadata (also called other files in general in context on this project) are included and checked against project expectations.

4. Project metadata is populated (dataset_description.json). This is required as a part of BIDS standard.

5. The dataset is registered in Dataverse and optionally pushed/uploaded automatically.

#### 1. Entry Point (`bids_process_and_upload()`)

- Reads project configuration (<project_name>_config.toml) to check if a other computer (non eeg files) was used. (otherFilesUsed: true)

- Iterates over each processed file and extracts identifiers. For example, for a file named `sub-001_ses-001_task-Default_run-001_eeg.xdf`, it extracts:

    - Subject ID (sub-XXX) - 001 (`str` is accepted)

    - Session ID (ses-YYY) - 001 (`str` is accepted)

    - Run number (run-ZZZ) - 001 (`int` is accepted)

    - Task name (task-Name) - Default (`str` is accepted)

- Constructs the absolute path to the .xdf file from the project root.

- Calls BIDS.convert_to_bids() to handle conversion and validation.

- After all files are processed:

- Populates dataset_description.json.

    - Generates JSON metadata (`generate_json_file.py`).

    - Creates/links a Dataverse dataset (`create_dataverse.py`).

    - Initializes a DataLad dataset and links with Dataverse (`create_and_add_files_to_datalad_dataset.py`, `add_sibling_dataverse_in_folder.py`).

    - Pushes data to Dataverse automatically (--yes) or via user confirmation.

#### 2. Convert to BIDS (`convert_to_bids()`)
This function handles the core conversion of a XDF files to BIDS format and constructs the dataset structure. It performs the following steps:

1. Copy raw/behavioral/experiment files via `copy_source_files_to_bids()` (See section).

2. Build a `BIDSPath` for the EEG recording:

    - Subject, session, run, task extracted from filename.

    - File format: EEGLAB (.set) chosen to avoid BrainVision memory issues.

3. The function checks if the BIDS file already exists:

    - If it does, it logs and doesn"t reconvert.

    - If --redo_bids_conversion is specified, it overwrites existing files. This flag is passed from the command line while running `lslautobids run`.

4. If the file doesn't exist or is to be overwritten, it proceeds with conversion:

    - Load `.xdf` with `create_raw_xdf()`. (See section).

    - Apply anonymization (daysback_min + anonymizationNumber from project TOML config).

    - Write EEG data into BIDS folder via `write_raw_bids().`

5. Validate results with `validate_bids()`. The function raises an error if validation fails and returns 0; otherwise returns 1 for success. (See section).

6. The convertt_to_bids() function returns a status code indicating the result of the conversion:

    - 1: Successful BIDS conversion and validation

    - 2: BIDS conversion already done i.e. file already existed, skipped conversion and validation

    - 0: BIDS Conversion done but validation failure

#### 3. Copy Source Files (`copy_source_files_to_bids()`)
This function ensures that the original source files (EEG and other/behavioral files) are also a part our dataset. These files can't be directly converted to BIDS format but we give the user the option to include them in the BIDS directory structure in a pseudo-BIDS format for completeness.

- Copies the .xdf into the following structure: 
`<BIDS_ROOT>/sourcedata/sub-XXX/ses-YYY/sub-XXX_ses-YYY_task-Name_run-ZZZ_eeg.xdf`

- Adds `_raw` suffix to distinguish original files.

- If a file already exists, logs a message and skips copying.

If otherFilesUsed=True in project config file:

1. Behavioral files are copied via `_copy_behavioral_files()`.

    - Validates required files against TOML config (`OtherFilesInfo`). In this config we add the the extensions of the expected other files. For example, in our testproject we use EyeList 1000 Plus eye tracker which generates .edf and .csv files. So we add these extensions as required other files. We also have mandatory labnotebook and participant info files in .tsv format.
    - Renames files to include sub-XXX_ses-YYY_ prefix if missing.
    - Deletes the other files in the project_other directory that are not listed in `OtherFilesInfo` in the project config file. It doesn"t delete from the source directory, only from out BIDS dataset.

2. Experimental files are copied via `_copy_experiment_files().`

    - Gathers files from the experiment folder.
    - Copies into BIDS `misc/` directory i.e. `<BIDS_ROOT>/misc/`
    - Compresses into experiment.tar.gz.
    - Removes the uncompressed folder.

There is a flag in the `lslautobids run` command called `--redo_other_pc` which when specified, forces overwriting of existing other and experiment files in the BIDS dataset. This is useful if there are updates or corrections to the other/behavioral data that need to be reflected in the BIDS dataset.

#### 4. Create Raw XDF (`create_raw_xdf()`)
This function reads the XDF file and creates an MNE Raw object. It performs the following steps:
- Select EEG stream using match_streaminfos(type="EEG").

- Resample to the highest nominal sampling rate across streams (fs_new).

- Read .xdf with `read_raw_xdf()`, enabling interpolation and marker prefixing.

- Annotate missing values (annotate_nan) and clean invalid annotations (negative onset).

- Map known channel labels to MNE channel types (e.g., heog → eog, bipoc → misc). This is done using a predefined dictionary of channel mappings for our lab setup. This can be extended in future versions to include user-defined mappings.

This produces a clean, memory-efficient Raw object ready for BIDS conversion.

#### 5. BIDS Validation (`validate_bids()`)
This function validates the generated BIDS files using the `bids-validator` package. It performs the following steps:
- Walks through the BIDS directory.
- Skips irrelevant files: (`.xdf`, `.tar.gz`, behavioral files, hidden/system files.)
- Uses `BIDSValidator` to validate relative paths. 
- If any file fails validation, logs an error and returns 0 ; Otherwise, logs success and returns 1.

#### 6. Populate dataset_description.json (`populate_dataset_description_json()`)
This function generates the `dataset_description.json` file required by the BIDS standard. It performs the following steps:
- Gathers metadata from the project configuration file (title, authors, license, etc.) from the project TOML config file.
- Calls make_dataset_description() from mne_bids.
- Overwrites existing file with updated values.

#### 7. Datalad and Dataverse Integration
This part of the pipeline manages version control and data sharing using DataLad and Dataverse. After conversion, the following steps occur:

- `generate_json_file()` → Generates supplementary metadata JSONs.
- `create_dataverse()` → Creates a new dataset in Dataverse. Returns DOI + status.
- `create_and_add_files_to_datalad_dataset()` → Initializes DataLad repo, adds files.
- `add_sibling_dataverse_in_folder()` → Links DataLad dataset to Dataverse (if new dataset).
- push_files_to_dataverse() uploads files to Dataverse. It automatically uploads if --yes is set (This flag is set in `lslautobids run`), otherwise the function prompts user (y/n).


### 4. DataLad Integration (`datalad_create.py`)

The DataLad integration module manages the creation and updating of DataLad datasets for version control of the BIDS dataset. This function initializes a DataLad dataset at a given project path.
The function performs the following steps:
1. Initialize commit message. It first sets a initialization message : "LSL Auto BIDS: new files found and added".
2. If flag == 0 (new dataset), the message is overwritten with "LSL Auto BIDS: new datalad dataset created".
3. Further, if flag == 0 we try to create a new DataLad dataset in the specified path (dataset_path) using `dl.create()`. This is similar to running `datalad create` from the command line for datalad CLI or `git init` for git CLI. This function is executed using :

`dl.create(dataset_path, force=True)`

Here, since the directory may already contain files (BIDS directory in our case), we use force=True to allow creation of the dataset even if files already exist and it is not an empty directory.

4. If it raises an exception (e.g., if the path is not a directory or if DataLad already exists ), it logs an error and exits the program.

5. This function also changes the current working directory to the dataset_path using `os.chdir(dataset_path)` so subsequent DataLad operations (like `datalad save`, `datalad push`) run in the context of this dataset.

6. This function also manages the .gitattributes file to ensure that large files are handled by git-annex and small text/metadata files are handled by git. This is done by appending specific patterns to the .gitattributes file. For example:
`*.csv annex.largefiles=nothing` means .csv files are treated as small files and stored directly in git. Similarly, *    annex.largefiles=largerthan=100kb` means files larger than 100kb are managed by git-annex.

7. Finally, it saves the changes to the DataLad dataset using `dl.save()` with the appropriate commit message. This save command stages all changes (new files, modified files) and commits them to the DataLad dataset.

8. If flag!=0 (existing dataset), it skips the initialization step and directly saves any new changes to the existing DataLad dataset.

### 5. Dataverse Integration

#### 1. Dataverse Dataset Creation (`dataverse_dataset_create.py`)
This module handles the creation of a new dataset in Dataverse using the `pyDataverse` library. The function performs the following steps:

1. Initialize `dataset.json` file path and read the JSON content. (See section)
2. Sets up a Dataverse API connection using the base URL and API key from the global configuration file (`autobids_config.yaml`). This dataset then loads the  `dataset.json` into the Dataset. This json metadata populates the dataset metadata in Dataverse (title, authors, description, etc.), where we will eventually upload our datalad compatible BIDS dataset.
3. The dataset JSON is validated using `ds.validate_json()`. If the validation passes only then we proceed to create the dataset in Dataverse using `dv.create_dataset()`.
4. The function also checks if that dataset already exists in Dataverse (based on title) to avoid duplicates. For example, one dataverse dataset can contain data from multiple participants/subjects and we usually create a single dataset for the entire project but run the conversion for each subject separately. So we check if a dataset with the same title already exists in Dataverse.
    - Get all the datasets (pids) in the specified parent dataverse using `api.get_dataverse(parent_dataverse_name)`.
    - Check if that the PID specified in the response matches the Dataverse PID specified in the project config file. If it does, we log a message and skip creation.
5. If no existing dataset is found, we create a new dataset using `api.create_dataset(parent_dataverse_name, ds.json())`. We then populate the returned dataset ID and DOI in the project configuration file (<project_name>_config.toml) for using in future runs.
6. This function returns the dataset DOI and status code ( 1= dataverse dataset exists, 0= new dataset created)

#### 2. Linking DataLad to Dataverse (`link_datalad_dataverse.py`)
This module links the local DataLad dataset to the remote Dataverse dataset as a sibling. The function performs the following steps:
1. It first checks if the Dataverse is already created in the previous runs or it is just created in the current run (flag==0). If flag==0, it proceeds to link the DataLad dataset to Dataverse.
2. It runs the command `datalad add-sibling-dataverse dataverse_base_url doi_id`. This command adds the Dataverse as a sibling to the local DataLad dataset, allowing for synchronization and data management between the two. For lslautobids, we currently only allow to deposit data to Dataverse. In future version, we shall also add user controlled options for adding other siblings like github, gitlab, OpenNeuro, AWS etc.

We chose Dataverse as it serves as both a repository and a data sharing platform, making it suitable for our needs. It also integrates well with DataLad and allows sharing datasets with collaborators or the public.

Dataverse also provides features like versioning, but only after we publish the dataset. In our case, we keep the dataset in draft mode until we are ready to publish it (i.e. until all the participants/subjects data is uploaded). So we use DataLad for version control during the development and conversion phase to assure complete provenance of the dataset.


#### 4 Generating dataset JSON Metadata (`generate_dataset_json.py`)

This module generates the `dataset.json` file required for creating a dataset in Dataverse. The function performs the following steps:

1. Gathers metadata from the project configuration file (<project_name>_config.toml) such as title, authors, description, license, etc.
2. Constructs a JSON structure that conforms to the Dataverse dataset metadata schema. This includes fields like title, author list, description, keywords, license, etc.
3. Writes the constructed JSON to a file named `dataset.json` in the project directory. This file is then used when creating the dataset in Dataverse.

#### 5. Upload to Dataverse (`upload_to_dataverse.py`)

This module handles the uploading of files from the local DataLad dataset to the remote Dataverse dataset. The function performs the following steps:
1. It runs the command `datalad push --to dataverse` to push the files from the local DataLad dataset to the linked Dataverse dataset. This command uploads all changes (new files, modified files) to Dataverse.
2. If the `--yes` flag is set (in `lslautobids run`), it automatically pushes the files without user confirmation. Otherwise, it prompts the user for confirmation before proceeding with the upload.

### Other Utility Modules

#### 1. Global Configuration Management (`config_globals.py`)
This module manages global configuration settings and command-line arguments using a singleton pattern. The `CLIArgs` class ensures that there is only one instance of the configuration throughout the application. It provides methods to parse and retrieve command-line arguments and global configuration settings (lslautobids_config.yaml), which are then used across various modules.

#### 2. Logging Configuration (`config_logger.py`)
This module sets up a global logger for the application. The `get_logger()` function creates and configures a logger instance with a specified project name. It ensures that all log messages are formatted consistently and that log levels are set appropriately. The final log file is stored in the `<BIDS_ROOT>/<project-name>/code/` folder of the BIDS dataset.

The log file is also available as a part of the created dataset.

#### 3. Utility Functions (`utils.py`)
This module contains various utility functions used across the application. 
1. `get_user_input` : Handles user prompts and input validation. This function allows five attempts for valid input before exiting. The function takes the user prompt message as an argument and returns the user input.
2. `read_toml_file` : Reads and parses a TOML file, returning its contents as a dictionary.
3. `write_toml_file` : Writes a dictionary to a TOML file.


## Testing

The testing framework uses `pytest` to validate the functionality of the core components.

- The tests are located in the `tests/` directory and cover various modules including configuration generation, file processing, BIDS conversion, DataLad integration, and Dataverse interaction. (Work in progress)

- The test directory contains :
    - `test_utils` : Directory containing utility functions needed across multiple test files.
    - `testcases` : Directory containing all the tests in a in a directory structure - `test_<test_name>`.
    - Each `test_<test_name>` directory contains a `data` folder with sample data for that test and a `test_<test_name>.py` file with the actual test cases.
    - `run_all_tests.py` : A script to run all the tests in the `testcases` directory sequentially.

Tests will be added continuously as new features are added and existing features are updated.

### Running Tests

To run the tests, navigate to the `tests/` directory and execute:
`python tests/run_all_tests.py`

These tests ensure that each component functions as expected and that the overall pipeline works seamlessly. This tests will also be triggered automatically on each push or PR to the main repository using GitHub Actions.

## Miscellianeous Points
- To the current date, only EEG data is supported for BIDS conversion. Support for other modalities like Eye-tracking, etc,. in the BIDS format is not yet supported. Hence, LSLAutoBIDS relies on semi-BIDS data structures for those data and use user-definable regular expressions to match expected data-files. A future planned feature is to provide users more flexibility, especially in naming / sorting non-standard files. Currently, the user can only specify the expected file extensions for other/behavioral data and is automatically renamed to include sub-XXX_ses-YYY_ prefix if missing and also copied to pseudo-BIDS folder structure like `<BIDS_ROOT>/sourcedata/sub-XXX/ses-YYY/`, `<BIDS_ROOT>/misc/experiment.tar.gz` etc,.

