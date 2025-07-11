
<h1 align="center">
  LSLAutoBIDS
</h1>
<p align="center"> Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse </p>


## 🚀 Getting Started

Get started with LSLAutoBIDS by installing the package and its dependencies.

## 🔰 About the package
This package automates the conversion of EEG recordings (xdf files) to BIDS (Brain Imaging Data Structure) format, integrates Datalad and uploads the data to  Dataverse. `lslautobids` is an open-source package written in `python` and  available as a pip package. 


## How to run the software?

### **Step 1: Clone the repository**
```
git clone https://github.com/s-ccs/LSLAutoBIDS.git
```
### **Step 2: Install the package**
```
pip3 install lslautobids
```
It is advised to install the package in a seperate environment (e.g. `conda`).

> [!NOTE]  
> If you are using conda, you can create a new conda environment using the following command and activate it.
```
conda create -n <ENV_NAME> python=3.11
conda activate <ENV_NAME>
```


### **Step 3: Data Organization**

The package requires the data to be organized in a specific directory structure which is compliant with the BIDS (Brain Imaging Data Structure) format. The BIDS format is a standard for organizing and describing neuroimaging data, making it easier to share and analyze.


- The `projects` root location is the root directory where all the eeg raw recordings (say `.xdf` files) are stored.
- The `project_stimulus` root location is the directory where the experiments (e.g `.py`, `.oxexp`) and behavioral files (e.g. eye-tracking recordings, labnotebook, participant forms, etc ) are stored.
- The `bids` root location is the directory where the converted BIDS data is stored, along with source data and code files which we want to version control using `Datalad`.

> [!IMPORTANT]
> Please follow the BIDS data organization guidelines for storing the neuroimaging data for running this package. The BIDS conversion guidelines are based on the recommended directory/files structure. You only can change the location of the root directories according to your preference. You must also strictly follow the naming convention for the project and subject subdirectories.

Here  you will find the recommended directory structure for storing the project data (recorded, stimulus and converted data) in the [data_organization](docs/data_organization.md) file.


### **Step 4: Generate the configuration files**

This configuration is required to run for running the automation pipeline of `lslautobids`. 

1. __AutoBIDS and Dataverse Configuration__ : 
- Run the command below to create a configuration file template in folder `~/.config/lslautobids/` folder. This will create a config file with the dataverse details and the root directories for the projects.         

```
lslautobids gen-dv-config
```
- Edit the file `autobids_config.yaml` to add the dataverse and project root details.

***This will be mostly same for all the projects, thus running this command is only recommended once per system.***

2. __Project Configuration__ : This is to be done once for each new project. This store the project details like project name, project id, project description etc.
- Run the command below to create a configuration file template in `/projects/<PROJECT_NAME>/` folder (according to the selected root directories).

```
lslautobids gen-proj-config -p <projectname> 
```
### **Step 6: Run the conversion scripts**

Run the conversion scripts to convert the xdf files to BIDS format and upload the data to the dataverse.
```
lslautobids gen-proj-config -p TestData2025
```
> [!NOTE]  
>You can run the `--help` for all the commands to get more information about the available options and directly `lsl-autobids help` to get the list of available commands.


## Disclaimer
The package is still in development and currently is only supported in MacOS and Linux. 

