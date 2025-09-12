# FAQ questions

1. What would be the process a user goes through if they collect additional data and wants to add them to the existing dataset? How automatic will this be?

- It is possible to re-run LSLAutoBIDS which would capture additional data from new subjects. Generally the idea is to run LSLAutoBIDS after each subject, then if there is an accidental overwrite we can still recover it due to versioning.

What Datalad commands are used currently in the workflow?
Answer : We use datalad save to add and version the current state of the dataset and datalad push  to push the current state to the remote repository. We do not use the datalad run and datalad rerun capabilities as of now in our tool.

How automated is addition / deletion of a sample (e.g. new subject)?
Answer: Right now, adding a new sample requires calling the lslautobids run command, which could be run silently as well (e.g. via a regular cronjob). Deleting a sample/subject is not currently supported by the tool, but could be performed via Datalad. This is by design. 
Do you generate a separate DOI for every dataset version? 
Answer: No, we have the same DOI current for the entire dataset, for all versions. Before publishing, we version the dataset via datalad using the same DOI, as Dataverse only supports versioning upon making the dataset public. 
 
Who controls the data upload process? 
Answer: There is a user prompt asking the experimenter if they want to upload the subject recording immediately when we run the lslautobids run command. We can also use the --yes flag of the lslautobids run command to force yes user input for all the user prompts throughout the run.

Can you upload a subset of files ?
Answer: Yes, we have configurations in the project_config.toml file where the experimenter can specify to exclude certain subjects, certain tasks, and only exclude private stimulus files.

Can you upload to any other portals apart from Dataverse? 
Answer: It is not yet implemented as a choice but rather hard coded, but as long as a dataverse sibling is supported, many portals could be used (dataverse, openneuro, aws,...). Currently, on Dataverse as a sibling is supported by our tool.


How do you handle data licensing?
Answer : Data license depends on the repository and can typically be chosen by the user typically upon making the dataset publicly available (or a data user agreement form can be employed). That being said, at OpenNeuro data is typically licensed CC0. 
