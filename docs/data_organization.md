# How the data is organized

In this project, we are using a sample xdf file along with the corresponding other files to demonstrate how the data inside the `projectname` folder is organized. This data should be organized in a specific way:

### Recommended Project Organization Structure 

For convenience, we have provided a recommended project organization  structure for the root directories to organize the data better.


> [!IMPORTANT]
> The recommended directory structure is not self generated. The user needs to create the directories and store the recorded and others data in them before running the conversion.

The dataset (both recorded and converted) is stored in the parent `data` directory. The `data` directory has three subdirectories under which the entire project is stored. The recommended directory structure is as follows:
```
data
├── bids                  # Converted BIDS data
  ├── projectname1
  ├── projectname2                
├── project_other      # Experimental/Behavioral files
  ├── projectname1
  ├── projectname2          
├── projects 
  ├── projectname1        # Recorded Raw data
  ├── projectname2 
             

```

Here `./data/projects/`, `./data/project_other/`, `./data/bids/` are the root project directories. Each of this root directories will have a project name directory inside it and each project directory will have a subdirectory for each subject. 


## Projects Folder

This folder contains the recorded raw files (`xdf files`). We save these files in a pseudo BIDS format. The folder structure is as follows:

        projectname/
        └── subject_id
            └── session_id
                └── datatype
                    └── datafiles

- **projectname** - any descriptive name for the project
- **subject_id** - `sub-<PARTICIPANTS_LABEL>` Eg: sub-001
- **session_id** - `ses-<PARTICIPANTS_LABEL>`. Eg: ses-001
- **datatype** - any of the following: eeg, beh, iee, meg, ieeg, mri, pet, other. Find more information about the datatypes [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/folders.html#datatype). For our project, we are using `eeg` as the datatype.
- **datafiles** - the data files for the corresponding datatype. Eg: ``sub-001_ses-001_task-Duration_run-001_eeg.xdf for our eeg data.`

Filename Convention for the raw data files :
`sub-<subjectlabel>_ses-<sessionlabel>_task-<tasklabel>_run-<runlabel>_ieeg.<extension>`
- **subjectlabel** - `001, 002, abc, XF, ...`
- **sessionlabel** - `001, 002, 003, ...`
- **tasklabel** - `duration, mscoco, ...`
- **runlabel** - `001, 002, 003, ...` (need to be an integer)

## Project Other Folder

This folder contains the experimental and behavioral files which we also store in the dataverse. The folder structure has to be as follows:

        projectname/
        └── experiment
            └── experimental_files (Matlab code, opensesame files, etc)
        └── data
            └── subject_id
                └── session_id
                    └── beh
                        └── behavioral_files((lab notebook, CSV, EDF file, etc))

It is possible to modify the `src=target` syntax to "skip" folders via `..` (maybe we should simply allow `{prefix}` in the src as well => not yet implemented)
- **projectname** - any descriptive name for the project
- **experiment** - contains the experimental files for the project. Eg: showOther.m, showOther.py
- **data** - contains the behavioral files for the corresponding subject. Eg: experimentalParameters.csv, eyetrackingdata.edf, results.tsv. 


You can get the filename convention for the data files [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/files.html#modalities).

## BIDS Folder

This folder contains the converted BIDS data files and other files we want to version control using `Datalad`. Since we are storing the entire dataset in the dataverse, we also store the raw xdf files and the associated other/behavioral files in the dataverse. The folder structure is as follows:
```
└── bids
  └──projectname/
    └── code
        └── log files
    
    └── sub-<label-sub>
        └── ses-<label-ses>
            └── datatype (eg: eeg)
                └── converted BIDS files
                    ├── sub-<label-sub>_ses-<label-ses>_task-Duration_run-001_eeg.vhdr
                    ├── sub-001_ses-001_task-Duration_run-001_eeg.vmrk
                    ├── sub-001_ses-001_task-Duration_run-001_eeg.eeg
                    .........
            └── misc (added to .bidsignore)
                └── experimental files (This needs to stored in zip format)
                └── labnotebook, subjectform etc. 
    └── sourcedata
        └── raw xdf files
    └── dataset_description.json
    └── participants.tsv
    └── participants.json
    └── README.md
```

- **projectname** - any descriptive name for the project
- **label** - `001, 002, 003, ...`
- **datatype** - any of the following: eeg, beh, iee, meg, ieeg, mri, pet, other. Find more information about the datatypes [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/folders.html#datatype).
