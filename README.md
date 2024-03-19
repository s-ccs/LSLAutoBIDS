
<h1 align="center">
  LSLAutoBIDS
</h1>
<p align="center"> Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse </p>


## 🚀 Getting Started

Get started with LSLAutoBIDS by installing the package and its dependencies.

## 🔰 About the package
This package automates the conversion of xdf files to BIDS format and uploads the data to a dataverse. The package is written in python and uses the pyxdf library to convert the xdf files to BIDS and the pyDataverse library to upload the data to the dataverse.


## Install the package

### Clone the github repository
```
git clone https://github.com/s-ccs/LSLAutoBIDS.git

```
## Install dependencies

It is advised to install the requirements in a seperate conda environment.

> [!NOTE]  
> If you are using conda, you can create a new conda environment using the following command and activate it.
```
conda create -n <ENV_NAME> python=3.12
conda activate <ENV_NAME>
```
Install the requirements using the following command inside the conda environment.
```
python -m pip install -r requirements.txt
```

 Install the datalad library using the following command[THIS STEP MIGHT NOT BE REQUIRED : CHECK!] :
```
conda install -c conda-forge datalad
```
If you donot have git and git-annex installed in your Operating System, you can install it seperately using the [datalad-installer](https://github.com/datalad/datalad-installer).

## Configuration and Data Organization
Dataset refers to the recorded eeg data in the xdf format.

A BIDS compliant dataset/project is organized in a specific directory structure. 
- The project root location is the directory where the recording is stored. 
- The project stimuli root location is the directory where the experimental and behavioral files are stored.
- The BIDS root location is the directory where the converted BIDS data is stored.

You can read more about the project data and file organization in the [data_organization](docs/data_organization.md) section.

> [!IMPORTANT]
> Please follow the BIDS data organization structure for storing the data. The BIDS conversion guidelines are based on the recommended directory/files structure. You only can change the location of the root directories according to your preference. You must also strictly follow the naming convention for the project and subject subdirectories.

### Recommended Project Organization Structure

For convenience, we have provided a recommended project organization  structure for the root directories to organize the data better.
You can directory skip to the [configuration](#configuration) section if you are not following the recommended directory structure.

> [!IMPORTANT]
> The recommended directory structure is not self generated. The user needs to create the directories and store the recorded and stimulus data in them.

The dataset (both recorded and converted) is stored in the parent `data` directory inside the `LSLAutoBIDS` directory. The `data` directory has three subdirectories:
```
data
├── bids                  # Converted BIDS data
├── project_stimulus      # Experimental files
├── projects              # Raw data

```
This `data` directory can be in the current project or home directory as per choice.

Here `./data/projects/`, `./data/project_stimulus/`, `./data/bids/` are the root project directories. Each of this root directories will have a project name directory inside it and each project directory will have a subdirectory for each subject. The data for each subject will be stored in the subject directory.

1. The raw recorded data needs to be stored in the `data/projects/<PROJECT_NAME>` directory i.e it will typically contain the xdf files.
2. The experimental and behavioral files need to be stored in the `data/project_stimulus/<PROJECT_NAME>` directory.
This folder contains two subfolders:
    - `experiment` folder contains the experimental files.
    - `sub-<SUBJECT_ID>`folder contains the behavioral files for each subject.
3. The converted BIDS data needs to be stored in the `data/bids/<PROJECT_NAME>` directory.

The `data/projects/<PROJECT_NAME>` directory has one  <PROJECT_NAME> folder for each project. Check [docs/data_organization.md](./docs/data_organization.md) for more details about the naming convention of the data.

TODO: For convenience there are some sample data in the [sample](./sample/) folder. You can copy the sample data to the `data` directory and run the scripts to see how the scripts work.

### Configuration 

This configuration is required to run the scripts. This scripts are to run from inside the `LSLAutoBIDS` directory. 
1. __AutoBIDS Project Configuration__ : This is to be done only once for all the projects if the dataverse and the root directory is the same.
- Run the command below to create a configuration file template in folder.

```
python gen_dv_config.py -p config_path

```
The config_path is the path where the configuration file will be stored. The default path is `autobids_config.yaml` in your '/home/username' directory
. 
- Edit the file `autobids_config.yaml` to add the dataverse details. Here the dataverse credentials and the root directories needs to be added. 

2. __Project Configuration__ : This is to be done once for each new project. This store the project details like project name, project id, project description etc.
- Run the command below to create a configuration file template in `/projects/<PROJECT_NAME>/` folder (according to the selected root directories).

```
python gen_project_config.py -p <PROJECT_NAME>

```
- Edit the configuration file in the `projects/<PROJECT_NAME>` folder to add the project details for the project.

TODO : Instructions about the fields to be added here


## Run the BIDS convertor

The conversion involves checking for new files to be converted, converting the files to BIDS and uploading the data to the dataverse. 

Run the following command to convert and upload the raw files.

```
python lsl_autobids/main.py -p <PROJECT_NAME> 

```

The `-p` flag is used to specify the project name. The project name is the name of the project directory in the `projects` directory.