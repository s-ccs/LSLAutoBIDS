
<h1 align="center">
  LSLAutoBIDS
</h1>
<p align="center"> Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse </p>


## 🚀 Getting Started

Get started with LSLAutoBIDS by installing the package and its dependencies.

```
# Using PyPI
python -m pip install lslautobids
```


## Install dependencies
```
python -m pip install -r requirements.txt
```

## Run the package

python -m scripts.main -p sampleproject


## Directory Structure

```
.
├── README.md        <- The top-level README with documentation and instructions for installing the project.
├── data             <- Data files for conversion and saving the bids data
│   ├── bids         <- BIDS converted data
│   │   ├── <projectname> <- project name of the currently converted data
│   │   │   ├── sub-01 <- subject number
│   │   │   │   ├── ses-01 <- session name
│   │   │   │   │   ├── eeg <- eeg data. Within this folder we have the bids files
│   │   │   ├── sourcedata <- store the raw xdf files
│   │   │   │   │   ├── sub-01 <- subject number
│   │   │   │   │   ├── ses-01 <- session name
│   │   │   │   │   │   ├── eeg <- eeg data . Within this folder we have the raw xdf file
│   └── projects     <- folder containing the raw xdf files
│   │   ├── <projectname> <- project name of the currently converted data
│   │   │   ├── sub-01 <- subject number
│   │   │   │   ├── ses-01 <- session name
│   │   │   │   │   ├── eeg <- eeg data. Within this folder we have the raw xdf file.
│   └── project_stimulus <- folder containing the experimental files
│   │   ├── <projectname> <- project name of the currently converted data
│   │   │   ├── sub-01 <- store the stimulus files for the subject
│   │   │   ├── experiment <- store the experiment scripts for the subject.
├── docs             <- Files containing documentation about the project
├── scripts          <- Source code for use in this project.
│   ├── __init__.py    <- Makes lslautobids a Python module
│   ├── main.py        <- main script to exceute the conversion
│   ├── upload.py      <- Functions for uploading to Dataverse
│   ├── processing.py <- Functions for processing the data with new files
│   └── bids.py       <- Functions relating to bids functionality
│    └── darus_config.py       <- Functions relating to bids functionality
├── tests            <- Unit tests
├── .gitignore       <- Files and folders to be ignored by git
├── requirements.txt <- The requirements file for reproducing the analysis environment.
├── setup.py         <- makes project pip installable (pip install -e .) so src can be imported
└── LICENSE          <- License file
```



## Resources- useful
 - https://earthly.dev/blog/python-makefile/
 - https://github.com/AUSSDA/dataverse2021_automation-with-pydataverse/tree/master