%% Convert data from .xdf to BIDS
close all; clear; clc;
cd '~/2022-MSc_EventDuration/experiments_matlab/mixed/exportBids'

filepath_bids = '~/2022-MSc_EventDuration/bids';
filepath_temp = '~/2022-MSc_EventDuration/temp';

% Run EEGLAB
eeglab;

%% Content for README file
README = 'MSc Thesis by Martin Geiger in 2022. Two experimental paradigms were carried out: P300 visual oddball task (Oddball) + N170 visual distracter task (Duration). Task Description - Oddball: The P300 component was elicited in an active visual oddball task, adapted from the ERP Core (Kappenman et al., 2021). The letters A, B, C, D, and E were presented in random order (p = .2 for each letter). For each block one letter was designated the target and the other 4 letters were distracters. Each letter was a target in 2 blocks and a distractor in the other 8 blocks. Participants responded whether the presented letter was the target or a distracter on each trial. Target-reponse mappings were randomized. Task Description – Duration: The N170 component was elicited in an active visual distracter task. Images of neutral faces, taken from the Chicago Face Database (Ma et al., 2015) were presented in random order. Subjects fixated a fixation cross in the screen center and responded when a red dot (=distracter) flickered in the center of the fixation cross. Distracters (p = .1 for each image) were spaced by at least 4 s.';

%% Content for CHANGES file
CHANGES = sprintf(['Version 1.0 - 28 Sep 2022\n' ...
                    ' - Initial release\n']); 

%% Participant column description for participants.json file
pInfoDesc.participant_id.Description = 'Unique participant identifier';
pInfoDesc.gender.Description         = 'Sex of participant';
pInfoDesc.gender.Levels.M            = 'Male';
pInfoDesc.gender.Levels.F            = 'Female';
pInfoDesc.age.Description            = 'Age of participant';
pInfoDesc.age.Units                  = 'Years';
pInfoDesc.handedness.Description     = 'Handedness of participant';
pInfoDesc.handedness.Levels.R        = 'Right';
pInfoDesc.handedness.Levels.L        = 'Left';
pInfoDesc.vision.Description         = 'Vision of participant';
pInfoDesc.vision.Levels.N            = 'Normal';
pInfoDesc.vision.Levels.C            = 'Corrected';

%% Code Files used to preprocess and import to BIDS
codefiles = { fullfile(pwd, mfilename) };

%% Loop through both tasks (Oddball and Duration)
for switchTask = 1:2
    if switchTask == 1
        task = 'Oddball';
    elseif switchTask == 2
        task = 'Duration';
    end

    %% General information for dataset_description.json file
    generalInfo.Name = 'P300 visual oddball task + N170 visual distracter task';
    generalInfo.ReferencesAndLinks = {'No bibliographic reference other than the DOI for this dataset'};
    generalInfo.BIDSVersion = 'v1.7.0';
    generalInfo.License = 'CC-BY';
    generalInfo.Authors = {'Martin Geiger'};

    %% Event column description for events.json file
    if switchTask == 1
        eInfo = {'onset'           'latency';
                'duration'         'duration';
                'sample'           'latency';
                'trial_type'       'type';
                'response_time'    'response_time'
                'keycode'          'keycode'
                'target_response'  'target_response'};
         
        eInfoDesc.keycode.Description  = 'Keycode for response';
        eInfoDesc.keycode.Levels.left  = '11';
        eInfoDesc.keycode.Levels.right = '12';
        eInfoDesc.targetResponse.Description  = 'Target-reponse mapping';
        eInfoDesc.targetResponse.Levels.left  = 'Left response (=keycode: 11) is correct for target trials with target_response=left';
        eInfoDesc.targetResponse.Levels.right = 'Right response (=keycode: 12) is correct for target trials with target_response=right';
    elseif switchTask == 2
        eInfoDesc = struct();
        eInfo = {'onset'           'latency';
                'duration'         'duration';
                'sample'           'latency';
                'trial_type'       'type';
                'response_time'    'response_time'};
    end

    %% Task information for eeg.json file
    tInfo.InstitutionName = 'University of Stuttgart';
    tInfo.InstitutionAddress = 'Universitätsstraße 34, 70569 Stuttgart, GER';
    tInfo.InstitutionalDepartmentName = 'Computational Cognitive Science';
    tInfo.Manufacturer = 'ANT Neuro';
    tInfo.ManufacturersModelName = 'EEG Cap: waveguard original cap (CA-203.s1). Amplifier: eego sports (EE-225).';
    if switchTask == 1
        tInfo.TaskDescription = 'The P300 component was elicited in an active visual oddball task, adapted from the ERP Core (Kappenman et al., 2021). The letters A, B, C, D, and E were presented in random order (p = .2 for each letter). For each block one letter was designated the target and the other 4 letters were distracters. Each letter was a target in 2 blocks and a distractor in the other 8 blocks. Participants responded whether the presented letter was the target or a distracter on each trial. Target-reponse mappings were randomized.';
        tInfo.Instructions = 'Throughout this experiment you will see a stream of letters (ABCDE). Your task is to respond to the letter that was displayed by pressing either the [TARGET_BUTTON] or [DISTRACTER_BUTTON], depending on the assignment given at the beginning of each block. You can take pauses between blocks if required. Press the buttons with your left and right index fingers. Maintain fixation on the cross in the screen center. Respond as quickly and accurately as possible.';
    elseif switchTask == 2
        tInfo.TaskDescription = 'The N170 component was elicited in an active visual distracter task. Images of neutral faces, taken from the Chicago Face Database (Ma et al., 2015) were presented in random order. Subjects fixated a fixation cross in the screen center and responded when a red dot (=distracter) flickered in the center of the fixation cross. Distracters (p = .1 for each image) were spaced by at least 4 s.';
        tInfo.Instructions = 'During this experiment faces will be presented, either without or with small breaks in between. Your task is to fixate the cross in the screen center and press the [BUTTON], as soon as you see a red dot flickering in the center of the cross. You can take pauses between blocks if required. Press the [BUTTON] with your right index finger. Respond as quickly as possible.';
    end
    tInfo.EEGReference = 'CPz';
    % tInfo.SamplingFrequency = 1000;
    tInfo.PowerLineFrequency = 50;
    tInfo.SoftwareFilter = 'n/a';
    % tInfo.EEGChannelCount = 60;
    % tInfo.EOGChannelCount = 4;
    % tInfo.EMGChannelCount = 0;
    % tInfo.ECGChannelCount = 0;
    tInfo.RecordingType = 'continuous';
    tInfo.EEGGround = 'left earlobe';
    tInfo.EEGPlacementScheme = '10-5';

    %% Read all .xdf files from study folder
    % Define paths
    xdfFolder = '/store/data/non-bids/MSc_EventDuration';
    fdtsetFolder = fullfile(filepath_temp,sprintf('fdtset_%s',task)); % Folder to save files in EEGLAB format
    addpath(genpath(xdfFolder));
    addpath(genpath(fdtsetFolder));

    % Check to make sure that study folder actually exists.  Warn user if it doesn't.
    if ~isfolder(xdfFolder)
        errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', xdfFolder);
        uiwait(warndlg(errorMessage));
        xdfFolder = uigetdir(); % Ask for a new one
        if xdfFolder == 0
            return; % User clicked 'cancel'
        end
    end

    % Get a list of all files in the folder with the desired file name pattern.
    if switchTask == 1
        filePattern = fullfile(xdfFolder,'**/*Oddball*.xdf');
        subjects = [4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41];
    elseif switchTask == 2
        filePattern = fullfile(xdfFolder,'**/*Duration*.xdf');
        subjects = [1 2 3 4 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 27 28 29 30 31 32 33 34 35 37 38 39 40 41];
    end
    theFiles = dir(filePattern);

    for i = subjects(1:end)
        if (switchTask == 2) && (i > 35)
            i = i-1;  %#ok<*FXSET>
            baseFileName = theFiles(i).name;
            fullFileName = fullfile(theFiles(i).folder, baseFileName);
            fprintf(1, 'Now reading %s\n', fullFileName);
            i = i+1;
        else
            baseFileName = theFiles(i).name;
            fullFileName = fullfile(theFiles(i).folder, baseFileName);
            fprintf(1, 'Now reading %s\n', fullFileName);
        end

        %% Load .xdf
        EEG = pop_loadxdf(fullFileName);

        %% Create events.tsv file in BIDS format
        eventsFile = tdfread(sprintf('~/2022-MSc_EventDuration/experiments_matlab/data/sub-%03i/ses-001/beh/sub-%03i_task-%s_events.tsv',i,i,task));
        if switchTask == 1
            events_tsv = struct('onset',[],'duration',[],'sample',[],'trial_type',[],'response_time',[],'condition',[],'keycode',[],'target_response',[]);
        elseif switchTask == 2
            events_tsv = struct('onset',[],'duration',[],'sample',[],'trial_type',[],'response_time',[]);
        end
        events_tsv.onset         = eventsFile.time;
        events_tsv.duration      = eventsFile.duration;
        events_tsv.trial_type    = eventsFile.eventName;
        events_tsv.response_time = eventsFile.reactionTime;
        if switchTask == 1
            events_tsv.condition       = eventsFile.condition;
            events_tsv.keycode         = eventsFile.keycode;
            events_tsv.target_response = eventsFile.targetResponse;
        end

        % Get latency from EEGlab struct
        EEG_copy = EEG;
        EEG_copy.event = struct2table(EEG_copy.event);
        markersEEG = [];
        markersLSL = [];
        for l = 1:length(EEG_copy.event.type)
            a = char(EEG_copy.event.type(l));
            % Split EEG and LSL markers
            if strcmp('@',a(2)) ||  strcmp('@',a(3))
                markersEEG{l} = EEG_copy.event(l,:);
            else
                markersLSL{l} = EEG_copy.event(l,:);
            end
        end
        % Sort according to latencies
        markersLSL = vertcat(markersLSL{:});
        sortedLSL = sortrows(markersLSL,2);
        % Add latency to events
        events_tsv.sample = sortedLSL.latency;

        events_tsv_bids = struct2table(events_tsv);

        m = 1;
        % Oddball
        if switchTask == 1
            for j = 1:length(events_tsv_bids.onset)
                if strcmp('buttonpress',events_tsv_bids.trial_type(j,:))
                    if strcmp('buttonpress',events_tsv_bids.trial_type(j-1,:))
                        events_tsv_bids.duration(j) = events_tsv_bids.duration(j-1);
                        continue
                    elseif (strcmp('stimOffset ',events_tsv_bids.trial_type(j-1,:))) && (strcmp('buttonpress',events_tsv_bids.trial_type(j-2,:)))
                        events_tsv_bids.duration(j) = events_tsv_bids.duration(j-2);
                        continue
                    end
                    for k = m:j
                        if events_tsv_bids.trial_type(k,:)=="stimOnset  "
                            if events_tsv_bids.trial_type(k+2,:)=="stimOnset  "
                                continue
                            end
                            events_tsv_bids.response_time(k) = events_tsv_bids.response_time(j);
                            events_tsv_bids.duration(j) = events_tsv_bids.duration(k);
                            m = k+1;
                        end
                    end
                end
            end
        % Duration
        elseif switchTask == 2
            for j = 1:length(events_tsv_bids.onset)
                if j == 383
                    asd = 1;
                end
                if strcmp('buttonpress ',events_tsv_bids.trial_type(j,:))
                    for k = m:j
                        if (events_tsv_bids.trial_type(k,:)=="stimOnset   ") && (events_tsv_bids.trial_type(k+1,:)=="targetOnset ")
                            events_tsv_bids.response_time(k+1) = events_tsv_bids.response_time(j);
                            events_tsv_bids.duration(j) = events_tsv_bids.duration(k);
                            m = k+1;
                        end
                    end
                end
            end
            % Rename targets to distracters
            events_tsv_bids.trial_type = cellstr(events_tsv_bids.trial_type);
            for j = 1:length(events_tsv_bids.onset)
                if strcmp('targetOnset',events_tsv_bids.trial_type(j))
                    events_tsv_bids.trial_type(j) = cellstr("distracterOnset");
                elseif strcmp('targetOffset',events_tsv_bids.trial_type(j))
                    events_tsv_bids.trial_type(j) = cellstr("distracterOffset");
                end
            end
            events_tsv_bids.trial_type = char(events_tsv_bids.trial_type);
        end

        %% Correct channel types
        EEG.chanlocs(32).type  = 'HEOG';
        EEG.chanlocs(32).units = 'microV';
        EEG.chanlocs(54).type  = 'HEOG';
        EEG.chanlocs(54).units = 'microV';
        EEG.chanlocs(57).type  = 'VEOG';
        EEG.chanlocs(57).units = 'microV';
        EEG.chanlocs(64).type  = 'VEOG';
        EEG.chanlocs(64).units = 'microV';
        EEG.chanlocs(65).type  = 'MISC';
        EEG.chanlocs(65).units = 'samples';

        %% Convert .xdf files (LSL) to .set files (EEGLAB)
        % Save as .set
        filename = sprintf('sub-%03i',i);
        pop_saveset(EEG,'filename',filename,'filepath',fdtsetFolder,'savemode','onefile');
        % Load .set file in EEGLAB
        filename = sprintf('sub-%03i.set',i);
        pop_loadset('filename',filename,'filepath',fdtsetFolder,'loadmode','all');

        %% Define data struct
        data = [];
        %p = fileparts(which('~/projects'));
        %data(end+1).file = { fullfile(p, 'bidsExport', sprintf('sub-00%i.set', k)) };
        if switchTask == 1
            data(i).task    = {'Oddball'};
        elseif switchTask == 2
            data(i).task    = {'Duration'};
        end
        data(i).file    = cellstr(fullfile(fdtsetFolder,filename)); %#ok<*SAGROW>
        data(i).session = 1;
        data(i).run     = 1;
        data(i).notes   = {'No notes'};

        %% Participant information for participants.tsv file
        pInfo = {'gender' 'age' 'handedness' 'vision'; % number of rows has to be equal to number of imported .set files
            'M' 25 'R' 'N'
            'M' 26 'R' 'N'
            'M' 29 'R' 'C'
            'M' 27 'R' 'C'
            'F' 29 'R' 'N'
            'M' 36 'R' 'N'
            'M' 28 'R' 'C'
            'M' 30 'R' 'N'
            'M' 27 'R' 'N'
            'M' 23 'R' 'N'
            'F' 26 'R' 'C'
            'F' 28 'R' 'C'
            'M' 30 'R' 'N'
            'M' 34 'R' 'C'
            'M' 24 'R' 'C'
            'M' 29 'R' 'N'
            'F' 26 'R' 'C'
            'M' 30 'R' 'N'
            'F' 30 'R' 'N'
            'M' 28 'R' 'N'
            'M' 26 'R' 'N'
            'F' 21 'R' 'N'
            'M' 32 'R' 'N'
            'M' 26 'R' 'C'
            'M' 30 'R' 'C'
            'M' 28 'R' 'N'
            'M' 27 'R' 'N'
            'W' 29 'R' 'N'
            'M' 23 'R' 'C'
            'F' 25 'R' 'C'
            'M' 30 'R' 'N'
            'F' 27 'R' 'N'
            'M' 33 'R' 'C'
            'F' 24 'R' 'N'
            'F' 25 'R' 'N'
            'M' 27 'R' 'N'
            'F' 22 'R' 'N'
            'F' 25 'R' 'N'
            'M' 22 'R' 'N'
            'F' 23 'R' 'N'
            'M' 23 'R' 'N'};

        pInfo = [pInfo(1,:);pInfo(1+i,:)];

        %% Export dataset to BIDS
        targetFolder =  fullfile(filepath_temp,sprintf('bids_%s/%03i',task,i));
        bids_export(data(i), ...
            'targetdir', targetFolder, ...
            'taskName', task,...
            'gInfo', generalInfo, ...
            'pInfo', pInfo, ...
            'pInfoDesc', pInfoDesc, ...
            'eInfo', eInfo, ...
            'eInfoDesc', eInfoDesc, ...
            'README', README, ...
            'CHANGES', CHANGES, ...
            'codefiles', codefiles, ...
            'renametype', {}, ...
            'checkresponse', 'condition 1', ...
            'tInfo', tInfo, ...
            'copydata', 1);

        %     'trialtype', trialTypes, ...

        %% Move and rename
        % Make directories in bids folder
        mkdir(fullfile(filepath_bids,sprintf('sub-%03i/ses-001/eeg',i)));
        % Rename and move files
        movefile(fullfile(filepath_temp,sprintf('bids_%s/%03i/sub-001/eeg/sub-001_task-%s_channels.tsv',task,i,task)),fullfile(filepath_bids,sprintf('sub-%03i/ses-001/eeg/sub-%03i_ses-001_task-%s_run-001_channels.tsv',i,i,task)));
        % movefile(fullfile(filepath_temp,sprintf('bids_%s/%03i/sub-001/eeg/sub-001_task-%s_eeg.fdt',task,i,task)),fullfile(filepath_bids,sprintf('sub-%03i/ses-001/eeg/sub-%03i_ses-001_task-%s_run-001_eeg.fdt',i,i,task)));
        movefile(fullfile(filepath_temp,sprintf('bids_%s/%03i/sub-001/eeg/sub-001_task-%s_eeg.json',task,i,task)),fullfile(filepath_bids,sprintf('sub-%03i/ses-001/eeg/sub-%03i_ses-001_task-%s_run-001_eeg.json',i,i,task)));
        movefile(fullfile(filepath_temp,sprintf('fdtset_%s/sub-%03i.set',task,i)),fullfile(filepath_bids,sprintf('sub-%03i/ses-001/eeg/sub-%03i_ses-001_task-%s_run-001_eeg.set',i,i,task)));
        writetable(events_tsv_bids,fullfile(filepath_bids,sprintf('sub-%03i/ses-001/eeg/sub-%03i_ses-001_task-%s_run-001_events.tsv',i,i,task)),'FileType','text','Delimiter','\t');
        % Move files
        if i == 41
            copyfile(fullfile(filepath_temp,sprintf('bids_%s/%03i/task-%s_events.json',task,i,task)),filepath_bids);
        end
        if (i == 41) && (switchTask == 1)
            copyfile(fullfile(filepath_temp,sprintf('bids_%s/%03i/dataset_description.json',task,i)),filepath_bids);
            copyfile(fullfile(filepath_temp,sprintf('bids_%s/%03i/CHANGES',task,i)),filepath_bids);
            copyfile(fullfile(filepath_temp,sprintf('bids_%s/%03i/participants.json',task,i)),filepath_bids);
            copyfile(fullfile(filepath_temp,sprintf('bids_%s/%03i/README',task,i)),filepath_bids);
            movefile(fullfile(filepath_temp,sprintf('bids_%s/%03i/code',task,i)),filepath_bids);
            movefile(fullfile(filepath_temp,sprintf('bids_%s/%03i/stimuli',task,i)),filepath_bids);
            copyfile(fullfile(filepath_temp,'participants.tsv'),filepath_bids);
        end
        % Delete rest
        rmdir(fullfile(filepath_temp,sprintf('bids_%s/%03i/',task,i)),'s')
    end
end

%% Validate BIDS format
addpath('~/MATLAB_Add-Ons/Collections/EEGLAB/plugins/bids-validator1.1');
pop_validatebids(filepath_bids)

