# Workflow updated
1. Use mnelab (which uses [pyxdf](https://github.com/xdf-modules/pyxdf)) python libary to load the xdf data and get the streams.[ Dont use MNE python here]
- The  xdf directory structure - Path specified in the projects folders to be specified in the LSL Recorder. It is automatically stored in the sub-xxx/ses-xxx structure.
- There can be multiple xdf files per subject (e.g. different tasks, or even stopped recordings, those should be renamed to "_ part-02.vhdr" => check in the recorder what happens if you try to overwrite a file, I think it is automatically renamed `One xdf file for each subject in our case.`
- Optional for now, let's focus on the conversion: `Check if new xdf file added to the folder`
- Stream names : EEGstream EE225 (fixed),eegoSports-EE225_markersMarkers(fixed) and LSL_Markers_<xxx>(variable-check with regex).
        -> We need a `metadata.toml`
```yml
authors: "Benedikt Ehinger"
title: "Awesome test study"
license: default #"This dataset is made available under the Public Domain Dedication and License \nv1.0, whose full text can be found at \nhttp://www.opendatacommons.org/licenses/pddl/1.0/. \nWe hope that all users will follow the ODC Attribution/Share-Alike \nCommunity Norms (http://www.opendatacommons.org/norms/odc-by-sa/); \nin particular, while not legally required, we hope that all users \nof the data will acknowledge the OpenfMRI project and NSF Grant \nOCI-1131441 (R. Poldrack, PI) in any publications.",
streams:
   EEG: "EEGstream EE225"
   marker: ["LSL_Markers","eegoSports-EE225_markersMarkers"] # will use the first if available, next one(s) as alternative
stimulusComputerUsed: true # will automatically copy experimental files & code from the mount point ~/project/stimulusComputer

# future thought?
# copypaths: 
#    - ~/project_stimulus/projectName/data/et/ => "et"
#    - ~/project_stimulus/projectName/data/behavioural/ => "misc"
```
        
- LSL Markers (time shifted but more effective) and EEG Markers (some disturbed) - [TODO to read].
- Check for the blank streams.[May be useful to retrieve the last stream id if we don't have the name]
- Resources to refer: 
    - [Reading xdf data](https://mne.tools/dev/auto_examples/io/read_xdf.html)
    - [Mamba installation of conda](https://mne.tools/stable/install/manual_install.html)


BIDS-MNE does the following:
        4. Write the description_dataset.json file. => `metadata.yml`
        6. Write the eeg.json file. The initial task description don't change. Sample frequency / number of channels => populate automatically
        8. electrode.tsv and channel.tsv. We use the extended 10-20 electrode setup from the mne python library to generate the electrode location from the .tsv file after generating the raw object file by pyxdf. => Later: add/rename "EOGs", find sensible defaults.

        5. Write the events.json file. => put a default events.json
                ```json
        {
    "marker_message": {
        "LongName": "Message of LSL or Trigger",
        "Description": "What experimental marker/trigger was send"
    }
}
```
        7. `events.tsv` => create automatically from Marker-Stream
```
onset   duration        marker_message
103.2   "n/a"   "LSL-Message / triggerNumber"
``` 
        2. Create a `participants.json` file (column desc male, female, sex, left, right etc) in the final BIDS directory. => fill automatically, skip description of optional fields later https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file
        9. Participants information for the .tsv file.
(fields in [optional] are optional)
        
```tsv 
participant_id  age     sex     handedness      [vision_corrected]      [dominant_eye]
sub-01  34      M       right   ["glasses"]     ["left"]
sub-02  33      D       left   ["no"]     ["right"]
```
        

10. Take the .xdf to BIDS format by mne python and [mne-bids](https://mne.tools/mne-bids/stable/use.html) and the BIDS structure directory with all the meta data will be generated in the form of triplet files. A text header file (.vhdr) containing meta data, a text marker file (.vmrk) containing information about events in the data,a binary data file (.eeg) containing the voltage values of the EEG.

- How do we specify the file structure which format to use. => mne-bids write command option
 - We use the [Brain Vision file format](https://mne.tools/dev/auto_tutorials/io/20_reading_eeg_data.html#brainvision-vhdr-vmrk-eeg).
 - [xdf to BIDS mne-python documentation](https://mne.tools/mne-bids/dev/auto_examples/convert_eeg_to_bids.html)
 - [BIDS datastructure specs](https://bids-standard.github.io/bids-starter-kit/index.html)#

## Copy Stimulus Computer Experimental Files
4. need to look for stimulus-computer experimental output files for that subject/run `projects_stimulus/projectName/sub-002/ses-001/.*`? => e.g. a `experiment_sub-002.mat` or `results-2.csv`. If yes, we need to include them into the BIDS datastructure `/sub-002/ses-001/misc`. `"experiment / stimulus files  should be written in advance [have to check in detail]. Task to run in specified in the LSL recorder.`    
4. (once) copy the experimental code to `bids/code/experiment/` from `~/projects_stimulusComputer/`

## validate BIDS
4. Validate the BIDS format
    
## upload to Darus
5. (once) create new darus repository + populate with `metadata.yml` info
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
    
    
future:
 -  `dataset_description.json` =>ReferencesAndLinks => DaRuS doi
 - UI to directly input participant_tsv information
