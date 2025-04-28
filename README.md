
<h1 align="center">
  LSLAutoBIDS
</h1>
<p align="center"> Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse </p>


## 🚀 Getting Started

Get started with LSLAutoBIDS by installing the package and its dependencies.

## 🔰 About the package
This package automates the conversion of xdf files to BIDS format and uploads the data to a dataverse. The package is written in python and uses the pyxdf library to convert the xdf files to BIDS and the pyDataverse library to upload the data to the dataverse.


## How to run the software?
### **Step 1: Clone the github repository**
```
git clone https://github.com/s-ccs/LSLAutoBIDS.git
```
### **Step 2: Navigate to the directory where the package is cloned.**
```
cd LSLAutoBIDS
```
### **Step 3: Install dependencies**

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

### **Step 4: Data Organization**

Dataset refers to the recorded eeg data in the `xdf` format.

A BIDS compliant dataset/project is organized in a specific directory structure. 
- The project root location is the root directory where all the recording are stored under a `<projectname>` directory.
- The project stimuli root location is the directory where the experiments and behavioral files are stored under a `<projectname>` directory.
- The BIDS root location is the directory where the converted BIDS data is stored under a `<projectname>` directory.

You can read more about the project data and file organization in the [data_organization](docs/data_organization.md) file.

> [!IMPORTANT]
> Please follow the BIDS data organization structure for storing the data in the `projectfolder`. The BIDS conversion guidelines are based on the recommended directory/files structure. You only can change the location of the root directories according to your preference. You must also strictly follow the naming convention for the project and subject subdirectories.

Here  you will find the recommended directory structure for storing the project data (recorded, stimulus and converted data) in the [data_organization](docs/data_organization.md) file.


### **Step 5: Generate the configuration files**

This configuration is required to run the scripts. This scripts are to run from inside the `LSLAutoBIDS` directory.
1. __AutoBIDS and Dataverse Configuration__ : 
- Run the command below to create a configuration file template in folder `~/.config/lslautobids/` folder. This will create a config file with the dataverse details and the root directories for the projects.         

```
python lsl_autobids/gen_dv_config.py
```
- Edit the file `autobids_config.yaml` to add the dataverse details.

***This will be mostly same for all the projects, thus creating only once per system is recommended.***

2. __Project Configuration__ : This is to be done once for each new project. This store the project details like project name, project id, project description etc.
- Run the command below to create a configuration file template in `/projects/<PROJECT_NAME>/` folder (according to the selected root directories).

```
python lsl_autobids/gen_project_config.py -p <PROJECT_NAME> -s no
```
Flags:
1. -p : Project name (required)
2. -s : toml_file standalone (optional , default is no.)
- Edit the configuration file in the `projects/<PROJECT_NAME>` folder to add the project details for the project if not used the standalone version.

### **Step 6: Run the conversion scripts**

Navigate to the project directory which you want to convert to BIDS format. 

```
cd path/to/your_project_directory/projectname
```

Run the autobids bash script to convert the xdf files to BIDS format and upload the data to the dataverse.

> [!IMPORTANT]
> The paths specified in the bash script might need to be changed according to your system and directory structure. Recheck the paths in the script before running it.
```
bash autobids.sh 
```
### Easy run after first time setup

After the first time setup, you can run the conversion script for each project using the following workflow:

Step 1 : Navigate to the LSLAutoBIDS package directory.
```
cd path/to/LSLAutoBIDS
```
Step 2 : Generate the configuration file for the new project.
```
python lsl_autobids/gen_dv_config.py # Optional, if we want to change the dataverse and root directories
```
````
python lsl_autobids/gen_project_config.py -p <PROJECT_NAME> -s no # Fill in the project details in the config file
````
Step 3 : Navigate to the project directory which you want to convert to BIDS format. 
```
cd path/to/your_project_directory/projectname
``` 
Step 4 : Run the autobids bash script to convert the xdf files to BIDS format and upload the data to the dataverse.
```
bash autobids.sh 
```



## Disclaimer
The package is still in development and currently is only supported in MacOS and Linux. 

