# How the data is organized

In this project, we are using a sample xdf file along with the corresponding stimulus files to demonstrate how the data inside the `projectname` folder is organized. This data should be organized in a specific way:

## Projects Folder
**Path:**  [../data/projects/projectname/](./data/projects/sampleproject)

This folder contains the recorded raw files (xdf files). We save these files in a pseudo BIDS format. This file along with some experimental parameters are used to generate the BIDS data files. The folder structure is as follows:

        projectname/
        └── subject_id
            └── session_id
                └── datatype
                    └── datafiles

- **projectname** - any descriptive name for the project
- **subject_id** - `sub-<PARTICIPANTS_LABEL>` Eg: sub-001
- **session_id** - `ses-<PARTICIPANTS_LABEL>`. Eg: ses-001
- **datatype** - any of the following: eeg, beh, iee, meg, ieeg, mri, pet, other. Find more information about the datatypes [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/folders.html#datatype).
- **datafiles** - the data files for the corresponding datatype. Eg: ``sub-001_ses-001_task-Duration_run-001_eeg.xdf for our eeg data.`

## Project Stimulus Folder
**Stimulus :** [./data/project_stimulus/projectname](./data/project_stimulus/sampleproject)

This folder contains the experimental and behavioral files which we also store in the dataverse. The folder structure is should as follows:

        projectname/
        └── experiment
            └── experimental_files (Matlab code, opensesame files, etc)
        └── data
            └── subject_id
                └── session_id
                    └── behavioral_files((lab notebook, CSV, EDF file, etc))

- **projectname** - any descriptive name for the project
- **experiment** - contains the experimental files for the project. Eg: showStimulus.m, showStimulus.py
- **data** - contains the behavioral files for the corresponding subject. Eg: experimentalParameters.csv, eyetrackingdata.edf, results.tsv. 

3. Filename Convention for the raw data files :
`sub-<subjectlabel>_ses-<sessionlabel>_task-<tasklabel>_run-<runlabel>_ieeg.<extension>`
- **subjectlabel** - `001, 002, 003, ...`
- **sessionlabel** - `001, 002, 003, ...`
- **tasklabel** - `duration, mscoco, ...`
- **runlabel** - `001, 002, 003, ...`

You can get the filename convention for the data files [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/files.html#modalities).

## BIDS Folder
[./data/bids/projectname](./data/bids/sampleproject)

This folder contains the converted BIDS data files. Since we are storing the entire dataset in the dataverse, we also store the raw xdf files and the associated stimulus/behavioral files in the dataverse. The folder structure is as follows:

        projectname/
        └── sub-<label>
            └── ses-<label>
                └── datatype (eg: eeg)
                    └── datafiles for eeg ()
                └── beh
                    └── datafiles for beh
                └── other
                    └── datafiles for other (This needs to stored in zip format)
        └── sourcedata
            └── raw xdf files
        └── dataset_description.json
        └── participants.tsv
        └── participants.json
        └── README


- **projectname** - any descriptive name for the project
- **label** - `001, 002, 003, ...`
- **datatype** - any of the following: eeg, beh, iee, meg, ieeg, mri, pet, other. Find more information about the datatypes [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/folders.html#datatype).
- **datafiles** - the data files for the corresponding datatype.
- **datafiles for eeg** - the data files obtained after converting the raw xdf files to BIDS format. Eg: `sub-001_ses-001_task-Duration_run-001_eeg.vhdr, sub-001_ses-001_task-Duration_run-001_eeg.vmrk, sub-001_ses-001_task-Duration_run-001_eeg.eeg` etc. The `participants.tsv`,`dataset_description.json` and `participants.json` files are also generated while converting the data to BIDS format.
- **datafiles for beh** - the data files copied from the behavioral files of the `project_stimulus` folder as shown in section [project stimulus folder](#project-stimulus-folder).
- **datafiles for other** - the data files copied from the experiment files of the `project_stimulus` folder as shown in section [project stimulus folder](#project-stimulus-folder).
- **sourcedata** - the raw xdf files stored in the dataverse.
