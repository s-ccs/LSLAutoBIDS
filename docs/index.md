<h1 align="center">
  LSLAutoBIDS
</h1>
<p align="center"> Tools to convert LSL + friends automatically to BIDS, and upload it to a Dataverse </p>


## 🚀 Getting Started

Get started with LSLAutoBIDS by installing the package and its dependencies.

## 🔰 About the package
This package automates the conversion of EEG recordings (xdf files) to BIDS (Brain Imaging Data Structure) format, integrates Datalad and uploads the data to  Dataverse. `lslautobids` is an open-source package written in `python` and  available as a pip package. 


## 🗒 Overview 

LSLAutoBIDS is a Python tool series designed to automate the following tasks sequentially:
- Convert recorded XDF files to BIDS format
- Integrate the EEG data with non-EEG data (e.g., behavioral, other) for the complete dataset 
- Datalad integration for version control for the integrated dataset
- Upload the dataset to Dataverse 
- Provide a command-line interface for cloning, configuring, and running the conversion process


### Key Features

- Automatic XDF to BIDS conversion
- DataLad integration for version control
- Dataverse integration for data sharing
- Configurable project management
- Support for behavioral data (non eeg files) in addition to EEG data
- Comprehensive logging and validation for BIDS compliance

For more details, refer to the paper - Automating Data Integration and Publishing for Neuroimaging via LSLAutoBIDS.