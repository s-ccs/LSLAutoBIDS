# Tutorial 
## Getting Started with LSLAutoBIDS

This tutorial will guide you through the steps to set up and use the LSLAutoBIDS package for converting EEG recordings to BIDS format, version controlling the data with Datalad, and uploading it to a Dataverse repository with a practical example.

### Installation and Download
1. Clone the Github Repository
```
git clone https://github.com/s-ccs/LSLAutoBIDS.git
```
2. Pip install the package
```
    cd LSLAutoBIDS
    pip install lslautobids
```
3. Download the dummy dataset for testing in the LSLAutoBIDS root directory - [download link]()

The dataset has a sample project called the test project "TestProject2025" which contains an EEG recording file (<insert filename here>) in the projects directory, a sample eyetracking recording in the project stimulus (<insert file names>)

### Configuration
1. Generate the global configuration file
```
lslautobids gen-dv-config
```
This will create a configuration file template in folder `~/.config/lslautobids/` folder. This will create a config file with the dataverse details and the root directories for the projects.

2. Create a Dataverse account and get the API token
- Create a dataverse account in your institution's dataverse server (e.g. https://darus.uni-stuttgart.de/dataverse/darus)
- Create a new dataverse for your project
- Create a new API token from your dataverse account settings page.

3. Open the configuration file `~/.config/lslautobids/autobids_config.yaml` and fill in the details
- Edit the file e.g. via `nano ~/.config/lslautobids/autobids_config.yaml` to add the dataverse and project root details.

Configuration file template:
```yaml
    "BIDS_ROOT": "# relative to home/users directory: LSLAutoBIDS/data/bids/",       
    "PROJECT_ROOT" : "# relative to home/users: LSLAutoBIDS/data/projects/", 
    "PROJECT_STIM_ROOT" : "# path relative to home/users: LSLAutoBIDS/data/project_stimulus/", 
    "BASE_URL": "https://darus.uni-stuttgart.de",  # The base URL for the service.
    "API_KEY": "# Paste your dataverse API token here", # Your API token for authentication.
    "PARENT_DATAVERSE_NAME": "simtech_pn7_computational_cognitive_science" # The name of the dataverse to which datasets will be uploaded. When you in the dataverses page , you can see this name in the URL after 'dataverse/'.
```
***This will be mostly same for all the projects, thus running this command is only recommended once per system.***

4. Create a project-specific configuration file
This will create a project-specific configuration file template in the specified project directory.

```
lslautobids gen-proj-config --project TestProject2025
```
Fill in the details in the configuration file `LSLAutoBIDS/data/projects/TestProject2025/TestProject2025_config.toml` file.

You can find the details about the parameters in the comments of the template configuration file generated. For this tutorial you might want to just change the author and email fields. Rest of the fields are already filled in for the test project.

## Example Case 1

A lab wants to conduct an EEG-EyeTracking experiment and wants to make this dataset  publicly available for the other neuroscience researchers. To assure data provenence and reproducibility within and across labs, they want to have a standardized structure for storing the data and code files. 

In this example we will see how to use the LSLAutoBIDS package to:
1. Convert the recorded EEG data in xdf format to BIDS format.
2. Integrate other data files (e.g. eye-tracking recording, experiment code files) into the dataset (Note: LSLAutoBIDS does not do any conversion of these files into BIDS format, it just copies these files to the appropriate directories in the BIDS dataset in a psuedo-BIDS like structure).
3. Version control the data and code files using Datalad.
4. Upload the dataset to a dataverse repository for public access.

### How to run the example?

1. Check if the toml configuration file `LSLAutoBIDS/data/projects/TestProject2025/TestProject2025_config.toml` is filled in with the correct details, specially the stimulusComputerUsed and expectedFiles fields. For this example we are using eye tracking data as a behavioral file, thus the stimulusComputerUsed field should be set to true and the expectedFiles field should contain the expected stimulus file extensions.
```toml
  [Computers]
    stimulusComputerUsed = true

  [ExpectedStimulusFiles]
    expectedFiles = [".edf", ".csv", "_labnotebook.tsv", "_participantform.tsv"]
```
2. Run the conversion and upload command to convert the xdf files to BIDS format and upload the data to the dataverse.
```
lslautobids run -p TestData2025
```

1. This will convert the xdf file in the `LSLAutoBIDS/data/projects/TestProject2025/sub-001/ses-001/eeg/` directory to BIDS format and store it in the `LSLAutoBIDS/data/bids/TestProject2025/sub-001/ses-001/` directory. 
2. You can check the logs in the log file `LSLAutoBIDS/data/bids/TestProject2025/code/TestProject2025.log` file. 
3. The source data i.e. the raw xdf file, behavioral data (e.g. eye-tracking recording) and the experimental code files in `PROJECT_STIM_ROOT/TestProject2025/experiment` (all files e.g. .py, .oxexp will be compressed to a `tar.gz` archive) will be copied to the `LSLAutoBIDS/data/bids/TestProject2025/source_data/`, `LSLAutoBIDS/data/bids/TestProject2025/beh/` and `LSLAutoBIDS/data/bids/TestProject2025/misc/` directories respectively.

## Example Case 2




## After publishing the dataset (Out of Scope of this package)

Once the dataset is published in dataverse, other researchers can access the dataset and also cite the dataset using the DOI provided by that dataverse dataset.

You can use clone the dataset using datalad and access the data files.

```
datalad clone <dataverse-dataset-url>
```

__Since the dataset is version controlled using datalad, the large files are not downloaded by default as they are stored in a git-annex. You can get the files using the datalad get command.__

```
datalad get <file-path>
```
