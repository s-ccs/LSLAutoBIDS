# Workflow
1. Use [pyxdf](https://github.com/xdf-modules/pyxdf) python libary to load the xdf data and get the streams.[ Dont use MNE python here]
- The  xdf directory structure - Path specified in the projects folders to be specified in the LSL Recorder. It is automatically stored in the subxxx/sesxxx structure.
- One xdf file for each subject in our case.
- Check if new xdf file added to the folder
- Stream names : EEGstream EE225 (fixed),eegoSports-EE225_markersMarkers(fixed) and LSL_Markers_<xxx>(variable-check with regex).
- LSL Markers (time shifted but more effective) and EEG Markers (some disturbed) - [TODO to read].
- Check for the blank streams.[May be useful to retrieve the last stream id if we don't have the name]
- Resources to refer: 
    - [Reading xdf data](https://mne.tools/dev/auto_examples/io/read_xdf.html)
    - [Mamba installation of conda](https://mne.tools/stable/install/manual_install.html)

2. Create a participants.json file (column desc male, female, sex, left, right etc) in the final BIDS directory.
3. Task files should be written in advance [have to check in detail]. Task to run in specified in the LSL recorder.
4. Write the description_dataset.json file. Project Independent.
5. Write the events.json file. [clueless].
6. Write the eeg.json file. The initial task description don't change. Sample frequency can be adjusted.
7. events.tsv ???
8. electrode.tsv and channel.tsv. We use the 1020 electrode setup from the mne python library to generate the electrode location from the .tsv file after generating the raw object file by pyxdf.
9. Participants information for the .tsv file.
 - Should there be any UI to directly integrate the user information into the code
 - Any format specifications of the information we need to collect.
10. Take the .xdf to BIDS format by mne python and [mne-bids](https://mne.tools/mne-bids/stable/use.html) and the BIDS structure directory with all the meta data will be generated in the form of tripet files. A text header file (.vhdr) containing meta data, a text marker file (.vmrk) containing information about events in the data,a binary data file (.eeg) containing the voltage values of the EEG.
 - How do we specify the file structure which format to use.
 - We use the [Brain Vision file format](https://mne.tools/dev/auto_tutorials/io/20_reading_eeg_data.html#brainvision-vhdr-vmrk-eeg).
 - [xdf to BIDS mne-python documentation](https://mne.tools/mne-bids/dev/auto_examples/convert_eeg_to_bids.html)
 - [BIDS datastructure specs](https://bids-standard.github.io/bids-starter-kit/index.html)
4. Validate the BIDS format
5. Upload it to Darus. 

[IN PROGRESS]
- Make unit test notebooks for all.
- Learn github project management.


[TODO]
1. Github project organization.
2. Take up a EEG processing course 
3. How the pipeline should look like. Is it running scripts with arguments or some UI?

[TO READ]
1. https://pressrelease.brainproducts.com/timing-verification/
2. https://www.youtube.com/watch?v=CbKPxwYPV9g [DONE]