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

## Directory structure

```
. 
├── README.md        <- The top-level README with documentation and instructions for installing the project.
├── data             <- Data files for testing
│   ├── bids         <- BIDS formatted data. It is in the folder structure data/bids/<projectname>/sub-01/ses-01/eeg/
│   └── projects     <- folder containing the raw xdf files. It is in the folder structure data/projects/<projectname>/sub-01/ses-01/eeg/
├── docs             <- Files containing documentation about the project
├── scripts          <- Source code for use in this project.
│   ├── __init__.py    <- Makes lslautobids a Python module
│   ├── main.py        <- Main script
│   ├── upload.py      <- Functions for uploading to Dataverse
│   ├── processing.py <- Functions for processing the data with new files
│   └── bids.py       <- Functions relating to bids functionality
├── tests            <- Unit tests
├── .gitignore       <- Files and folders to be ignored by git
├── requirements.txt <- The requirements file for reproducing the analysis environment,
├── setup.py         <- makes project pip installable (pip install -e .) so src can be imported
└── tests         <- Unit tests

```


## Resources- useful
 - https://earthly.dev/blog/python-makefile/