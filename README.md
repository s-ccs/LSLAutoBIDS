# LSLAutoBIDS
Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse

The testcode folder has some sample .xdf and files in BIDS format for testing purpose.

## Install dependencies

python -m pip install -r requirements.txt

For datalad-dataverse

```
pip install datalad

pip install datalad-dataverse

datalad create -d ./data/datalad-dataset --force

cd ./data/datalad-dataset

datalad status

datalad save -m "Initial commit"

datalad add-sibling-dataverse https://darus.uni-stuttgart.de/ doi:10.18419/darus-3520

datalad push --to dataverse

git remote -v () copy the url from here

datalad clone 'datalad-annex::?type=external&externaltype=dataverse&encryption=none&exporttree=no&url=https%3A//darus.uni-stuttgart.de/&doi=doi:10.18419/darus-3520' myclone

datalad siblings -d "myclone" enable -s dataverse-storage

datalad get my-file
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