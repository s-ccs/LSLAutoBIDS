## BIDS Conversion and Upload Pipeline ⚙️ (`convert_to_bids_and_upload.py`)

The pipeline is designed to ensure:

1. Source files (EEG only) are preserved in a BIDS-compatible structure.

2. EEG recordings are converted to BIDS format using MNE and validated against the BIDS standard.

3. Behavioral and experimental metadata (also called other files in general in context on this project) are included and checked against project expectations.

4. Project metadata is populated (dataset_description.json). This is required as a part of BIDS standard.

5. The dataset is registered in Dataverse and optionally pushed/uploaded automatically.

#### Entry Point (`bids_process_and_upload()`)

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

#### Convert to BIDS (`convert_to_bids()`)
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

#### Copy Source Files (`copy_source_files_to_bids()`)
This function ensures that the original source files (EEG and other/behavioral files) are also a part our dataset. These files can't be directly converted to BIDS format but we give the user the option to include them in the BIDS directory structure in a pseudo-BIDS format for completeness.

- Copies the .xdf into the following structure: 
`<BIDS_ROOT>/sourcedata/sub-XXX/ses-YYY/sub-XXX_ses-YYY_task-Name_run-ZZZ_eeg.xdf`

- Adds `_raw` suffix to distinguish original files.

- If a file already exists, logs a message and skips copying.

If otherFilesUsed=True in project config file:

1. Behavioral files are copied via `_copy_behavioral_files()`.

    - Validates required files against TOML config (`OtherFilesInfo`). In this config we add the the extensions of the expected other files. For example, in our testproject we use EyeList 1000 Plus eye tracker which generates .edf and .csv files. So we add these extensions as required other files. We also typically have mandatory labnotebook and participant info files in .tsv format.
    - The `"*.src"="beh/{prefix}_target"` allows users to easily add BIDS-compatible custom data from the experiments. Note that `json` sidecars are not automatically generated yet.
    

2. Experimental files are copied via `_copy_experiment_files().`

    - Gathers files from the `<PROJECTS_OTHER>/experiment/` folder.
    - Copies into BIDS `misc/` directory i.e. `<BIDS_ROOT>/misc/`
    - Compresses into `experiment.tar.gz`.
    - Removes the uncompressed folder.

There is a flag in the `lslautobids run` command called `--redo_other_pc` which when specified, forces overwriting of existing other and experiment files in the BIDS dataset. This is useful if there are updates or corrections to the other/behavioral data that need to be reflected in the BIDS dataset.

#### Create Raw XDF (`create_raw_xdf()`)
This function reads the XDF file and creates an MNE Raw object. It performs the following steps:
- Select EEG stream using match_streaminfos(type="EEG").

- Resample to the highest nominal sampling rate across streams (fs_new).

- Read .xdf with `read_raw_xdf()`, enabling interpolation and marker prefixing.

- Annotate missing values (annotate_nan) and clean invalid annotations (negative onset).

- Map known channel labels to MNE channel types (e.g., heog → eog, bipoc → misc). This is done using a predefined dictionary of channel mappings for our lab setup. This can be extended in future versions to include user-defined mappings.

This produces a clean, memory-efficient Raw object ready for BIDS conversion.

#### BIDS Validation (`validate_bids()`)
This function validates the generated BIDS files using the `bids-validator` package. It performs the following steps:
- Walks through the BIDS directory.
- Skips irrelevant files already ignored in `.bidsignore` (`misc` folder, some hidden files)
- Uses `BIDSValidator` to validate relative paths. 
- If any file fails validation, logs an error and returns 0 ; Otherwise, logs success and returns 1.

#### Populate dataset_description.json (`populate_dataset_description_json()`)
This function generates the `dataset_description.json` file required by the BIDS standard. It performs the following steps:
- Gathers metadata from the project configuration file (title, authors, license, etc.) from the project TOML config file.
- Calls make_dataset_description() from mne_bids.
- Overwrites existing file with updated values.

#### Datalad and Dataverse Integration
This part of the pipeline manages version control and data sharing using DataLad and Dataverse. After conversion, the following steps occur:

- `generate_json_file()` → Generates supplementary metadata JSONs.
- `create_dataverse()` → Creates a new dataset in Dataverse. Returns DOI + status.
- `create_and_add_files_to_datalad_dataset()` → Initializes DataLad repo, adds files.
- `add_sibling_dataverse_in_folder()` → Links DataLad dataset to Dataverse (if new dataset).
- push_files_to_dataverse() uploads files to Dataverse. It automatically uploads if --yes is set (This flag is set in `lslautobids run`), otherwise the function prompts user (y/n).

