# Workflow
1. Use [pyxdf](https://github.com/xdf-modules/pyxdf) python libary to load the xdf data and get the streams.[ Dont use MNE python here]
- Where do I find the .xdf file? 
- The file structure?
- One xdf file for each subject?
- The filename format
- What preprocessing required (may be some annotations)
- Resources to refer: 
    - [Reading xdf data](https://mne.tools/dev/auto_examples/io/read_xdf.html)
    - [Mamba installation of conda](https://mne.tools/stable/install/manual_install.html)

2. Create a participants.json file ?
3. Participants information for the .tsv file.
 -  Should there be any UI to directly integrate the user information into the code
- Any format specifications of the information we need to collect.
3. Take the .xdf to BIDS format by mne python.
 - Where we need to integrate the participants data in the BIDS format?
 - How do we specify the file structure which format to use.
 - We use the [Brain Vision file format](https://mne.tools/dev/auto_tutorials/io/20_reading_eeg_data.html#brainvision-vhdr-vmrk-eeg).
 - [xdf to BIDS mne-python documentation](https://mne.tools/mne-bids/dev/auto_examples/convert_eeg_to_bids.html)
 - mne bids should write down the  electrode coordinate information (electrode.tsv)(how to get that for our setup)
 - 
4. Validate the BIDS format
5. Upload it to Darus. 

- Make unit test notebooks for all.


# Project Organization
1. Github project organization.
- Any specfic format for the github.



To figure out:
1. Does stream dict represent metadata about that event from the subject? See read_and_load_xdf_files notebook
2. 
