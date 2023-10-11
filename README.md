
<h1 align="center">
  LSLAutoBIDS
</h1>
<p align="center"> Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse </p>


## 🚀 Getting Started

Get started with LSLAutoBIDS by installing the package and its dependencies.

## 🔰 About the package
This package automates the conversion of xdf files to BIDS format. It also uploads the data to a dataverse. We are using the dataverse at the University of Stuttgart. The package is written in python and uses the pyxdf library to convert the xdf files to BIDS and the pyDataverse library to upload the data to the dataverse.


## Install the package

### Clone the github repository
```
git clone -b working --single-branch https://github.com/s-ccs/LSLAutoBIDS.git

```
## Install dependencies
```
python -m pip install -r requirements.txt
```

If you get an error while installing the datalad library, try installing the datalad library using the following command:
```
conda install -c conda-forge datalad
```

## Dataset

The dataset is stored in the [data](./data/) directory. The data directory has three subdirectories:

1. The raw recorded data needs to be stored in the [`data/projects/<PROJECT_NAME>`](./data/projects/) directory i.e it will typically contain the xdf files.
2. The experimental files need to be stored in the [`data/project_stimulus/<PROJECT_NAME>`](./data/project_stimulus/) directory.
This folder contains two subfolders:
    - [`experiment`](./data/project_stimulus/sampleproject/experiment/) folder contains the experimental files.
    - [`sub-<SUBJECT_ID>`](./data/project_stimulus/sampleproject/sub-004/) folder contains the experimental files for each subject.
3. The converted BIDS data needs to be stored in the [`data/bids/<PROJECT_NAME>`](./data/bids/) directory.

The [`data/projects/<PROJECT_NAME>`](./data/projects/) directory has one  <PROJECT_NAME> folder for each project. Check [docs/data_organization.md](./docs/data_organization.md) for more details about the naming convention of the data.

Note: The [`data/projects/<PROJECT_NAME>`](./data/projects/) and [`data/project_stimulus/<PROJECT_NAME>`](./data/project_stimulus/) directories are not created by the package. The user needs to create these directories and store the data in them. For convenience there are some sample data in the [sample_data](./sample_data/) folder.

## Configuration

1. Run the command below to create a configuration file template in ./data/projects/<PROJECT_NAME>/ folder.

```
python config_info.py -p <PROJECT_NAME>

```
2. Edit the configuration file to add the project details for the project.

## Run the scripts






## Run the package [TODO]

python -m scripts.main -p sampleproject


## Directory Structure

```
.
├── data
│   ├── bids
│   │   └── sampleproject
│   │       ├── dataset_description.json 
│   │       ├── participants.json 
│   │       ├── participants.tsv 
│   │       ├── README 
│   │       ├── sourcedata
│   │       │   └── sub-004
│   │       │       └── ses-001
│   │       │           └── eeg
│   │       │               └── sub-004_ses-001_task-Duration_run-001_eeg_raw.xdf
│   │       └── sub-004
│   │           └── ses-001
│   │               ├── beh
│   │               │   ├── sub-004_ses-001_task-Duration_run-001_experimentalParameters.csv 
│   │               │   ├── sub-004_ses-001_task-Duration_run-001_eyetrackingdata.edf 
│   │               │   └── sub-004_ses-001_task-Duration_run-001_results.tsv 
│   │               ├── eeg
│   │               │   ├── sub-004_ses-001_task-sampleproject_channels.tsv 
│   │               │   ├── sub-004_ses-001_task-sampleproject_eeg.eeg 
│   │               │   ├── sub-004_ses-001_task-sampleproject_eeg.json 
│   │               │   ├── sub-004_ses-001_task-sampleproject_eeg.vhdr 
│   │               │   ├── sub-004_ses-001_task-sampleproject_eeg.vmrk 
│   │               │   └── sub-004_ses-001_task-sampleproject_events.tsv 
│   │               ├── other
│   │               │   ├── sub-004_ses-001_task-Duration_run-001_showStimulus.m 
│   │               │   └── sub-004_ses-001_task-Duration_run-001_showStimulus.py 
│   │               └── sub-004_ses-001_scans.tsv 
│   ├── projects
│   │   └── sampleproject
│   │       ├── last_run_log.txt
│   │       ├── project.toml
│   │       └── sub-004
│   │           └── ses-001
│   │               └── eeg
│   │                   └── sub-004_ses-001_task-Duration_run-001_eeg.xdf
│   └── project_stimulus
│       └── sampleproject
│           ├── experiment
│           │   ├── showStimulus.m
│           │   └── showStimulus.py
│           └── sub-004
│               ├── experimentalParameters.csv
│               ├── eyetrackingdata.edf
│               └── results.tsv
├── docs
│   └── about.md
├── empty_log_file_temp.py [TEMPORARY]
├── LICENSE
├── lsl_autobids
│   ├── bids.py
│   ├── darus_config.json
│   ├── datalad_create.py
│   ├── dataset.json
│   ├── dataverse_dataset_create.py
│   ├── folder_config.py
│   ├── generate_dataset_json.py
│   ├── __init__.py
│   ├── link_datalad_dataverse.py
│   ├── main.py
│   ├── processing.py
├── README.md
├── requirements.txt
├── setup.py
├── tests
└── TODO.md
```



1. The [`data`](./data/) directory has one  <PROJECT_NAME> folder for each project. Each project folder has the following structure:
    - [`bids`](./data/bids/sampleproject/) folder contains the converted bids data files.
    - [`projects`](./data/projects/sampleproject/) folder contains the raw xdf files.
    - [`project_stimulus`](./data/project_stimulus/sampleproject/) folder contains the experimental files.
More details about the directory structure can be found in the [´docs/bids_data_structure´](./docs/bids_data_structure.md) file.
2. The [`docs`](./docs/) directory contains the documentation of the project.
    -  [about.md](./docs/about.md) contains the description and organization of the project.
    -  [bids_data_structure.md](./docs/bids_data_structure.md) contains the description of the directory structure of the data directory.


## Resources- useful
 - https://earthly.dev/blog/python-makefile/
 - https://github.com/AUSSDA// 
 - dataverse2021_automation-with-pydataverse/tree/master
 - https://psychoinformatics-de.github.io/rdm-course/02-structuring-data/index.html