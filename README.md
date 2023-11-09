
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
git clone https://github.com/s-ccs/LSLAutoBIDS.git

```
## Install dependencies

It is advised to install the requirements in a seperate conda environment.s
```
python -m pip install -r requirements.txt
```

 Install the datalad library using the following command:
```
conda install -c conda-forge datalad
```
If you donot have git and git-annex installed in your Operating System, you can give the installation instructions in the [datalad handbook.](https://handbook.datalad.org/en/latest/intro/installation.html.)

## Dataset

The dataset is stored in the [data](./data/) directory. The data directory has three subdirectories:

> [!NOTE]  
> This project root locations can be changed manually in the [data_config.yaml](data_config.yaml). However, wherever you store the data, the projects under the projects and the project_stimulus directories expect a structure of organizing each project and subject data as described in [data_organization](docs/data_organization.md).

If you use the recommended directory structure, the data directory will look like the following and you can follow the following instructions to store the data and if not you can skip this part and directly go to the [configuration](#configuration) section.

```
data
├── bids
├── project_stimulus
├── projects

```
Here './data/projects/', './data/project_stimulus/', './data/bids/' are the root project directories. Each of this root directories will have a project name directory inside it and each project directory will have a subdirectory for each subject. The data for each subject will be stored in the subject directory.

1. The raw recorded data needs to be stored in the [`data/projects/<PROJECT_NAME>`](./data/projects/) directory i.e it will typically contain the xdf files.
2. The experimental files need to be stored in the [`data/project_stimulus/<PROJECT_NAME>`](./data/project_stimulus/) directory.
This folder contains two subfolders:
    - [`experiment`](./data/project_stimulus/sampleproject/experiment/) folder contains the experimental files.
    - [`sub-<SUBJECT_ID>`](./data/project_stimulus/sampleproject/sub-004/) folder contains the experimental files for each subject.
3. The converted BIDS data needs to be stored in the [`data/bids/<PROJECT_NAME>`](./data/bids/) directory.

The [`data/projects/<PROJECT_NAME>`](./data/projects/) directory has one  <PROJECT_NAME> folder for each project. Check [docs/data_organization.md](./docs/data_organization.md) for more details about the naming convention of the data.

Note: The [`data/projects/<PROJECT_NAME>`](./data/projects/) and [`data/project_stimulus/<PROJECT_NAME>`](./data/project_stimulus/) directories are not self generated. The user needs to create these directories and store the data in them. 

TODO: For convenience there are some sample data in the [sample_data](./sample_data/) folder.

## Configuration 

This configuration is required to run the scripts. 

1. __Project Configuration__ : This is to be done once for each new project. This store the project details like project name, project id, project description etc.
- Run the command below to create a configuration file template in ./data/projects/<PROJECT_NAME>/ folder.

```
python gen_project_config.py -p <PROJECT_NAME>

```
- Edit the configuration file in the projects folder to add the project details for the project.

2. __Dataverse Credentials Configuration__ : This is to be done only once, for all the projects if the dataverse is the same.
- Run the command below to create a configuration file template in folder.

```
python gen_dv_config.py 

```
- Edit the file [dataverse_config.yaml](dataverse_config.yaml) to add the dataverse details. Here the dataverse url, api token and the parent dataverse needs to be added. 


## Run the BIDS convertor

The conversion involves checking for new files to be converted, converting the files to BIDS and uploading the data to the dataverse. 

Run the following command to convert and upload the raw files.

```
python lsl_autobids/main.py -p <PROJECT_NAME> 

```

# Directory Structure

```
.
├── data                          # Data directory
│   ├── bids                      # BIDS data directory
│   ├── project_stimulus          # Experimental files directory
│   ├── projects                  # Raw data directory
├── docs                          # Documentation directory
├── lsl_autobids                  # Package directory
│   ├── __init__.py
│   ├──  main.py                  # Main script to run the package
│   ├──  processing.py            # Script to process the data
│   ├── convert_to_bids_and_upload.py # Script to convert to BIDS and upload to dataverse

│   
## Resources- useful
 - https://earthly.dev/blog/python-makefile/
 - https://github.com/AUSSDA// 
 - dataverse2021_automation-with-pydataverse/tree/master
 - https://psychoinformatics-de.github.io/rdm-course/02-structuring-data/index.html