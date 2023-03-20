#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 22:40:58 2023

@author: geiger
"""

from pyxdf import match_streaminfos, resolve_streams
from mnelab.io.xdf import read_raw_xdf
import mne
import matplotlib.pyplot as plt
import numpy as np

#%% Load data

# Paths
filepath = '/home/geiger/github/LSLAutoBIDS/starters/raw_xdf/sub-004/ses-001/eeg/'
filename = 'sub-004_ses-001_task-Oddball_run-001_eeg.xdf'

# Get streams
streams = resolve_streams(filepath + filename)
id_eeg = match_streaminfos(streams, [{"name": "EEGstream EE225"}])[0]
id_eeg_markers = match_streaminfos(streams, [{"name": "eegoSports-EE225_markersMarkers"}])[0]
id_lsl_markers = match_streaminfos(streams, [{"name": "LSL_Markers_Matlab"}])[0]

#%% mne raw object

# Create raw object
raw = read_raw_xdf(filepath + filename, stream_ids=[id_eeg])

# Investigate raw object
raw.annotations
raw.info
raw.info['ch_names']

# If you want to drop a channel, e.g. sampleNumber
#raw.drop_channels(["sampleNumber"])

# Events
events = mne.events_from_annotations(raw)
# eeg_markers are of form 'int@int' e.g. '48@1103505' meaning 'eventCode@sample'
# lsl_markers are of form 'string:float' e.g. 'buttonpress:157.0615' meaning 'event:time[s]'

#%% Plot data

# Extract a channel by name
sfreq = raw.info['sfreq']
start_stop_seconds = np.array([0, 250])
start_sample, stop_sample = (start_stop_seconds * sfreq).astype(int)
# One channel:
channel_names = ['Pz']
# All channels:
#channel_names = raw.info['ch_names'][0:63]
raw_selection = raw[channel_names, start_sample:stop_sample]

# Plot data
t = raw_selection[1]
signal = raw_selection[0].T
plt.plot(t, signal)

