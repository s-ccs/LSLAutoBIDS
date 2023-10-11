# How the data is organized

In this project, we are using a sample xdf file along with the corresponding stimulus files to demonstrate how the data is organized. The data is organized in the following way:


1. [./data/projects/PROJECTNAME](./data/projects/sampleproject)

This folder contains the recorded raw files. We save the raw files in a pseudo BIDS format. This file along with some experimental parameters are used to generate the BIDS data files. The folder structure is as follows:

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


2. [./data/project_stimulus/PROJECTNAME](./data/project_stimulus/sampleproject)

This folder contains the experimental and behavioral files which we also store in the dataverse. The folder structure is as follows:

        projectname/
        └── experiment
            └── experimental_files
        └── subject_id
            └── behavioral_files

- **projectname** - any descriptive name for the project
- **experiment** - contains the experimental files for the project. Eg: showStimulus.m, showStimulus.py
- **subject_id** - contains the behavioral files for the corresponding subject. Eg: experimentalParameters.csv, eyetrackingdata.edf, results.tsv

3. Filename Convention for the raw data files :
`sub-<subjectlabel>_ses-<sessionlabel>_task-<tasklabel>_run-<runlabel>_ieeg.<extension>`

*The parts under the square brackets are optional.*

You can get the filename convention for the data files [here](https://bids-standard.github.io/bids-starter-kit/folders_and_files/files.html#modalities).

4.  [./data/bids/PROJECTNAME](./data/bids/sampleproject)

This folder contains the converted BIDS data files. Since we are storing the entire dataset in the dataverse, we also store the raw xdf files and the associated stimulus/behavioral files in the dataverse. The folder structure is as follows:

        projectname/
        └── sub-<label>
            └── ses-<label>
                └── datatype (eg: eeg)
                    └── datafiles for eeg
                └── beh
                    └── datafiles for beh
                └── other
                    └── datafiles for other
        └── sourcedata
            └── raw xdf files
        └── dataset_description.json
        └── participants.tsv
        └── participants.json
        └── README