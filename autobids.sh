#!/bin/bash
eval "$(conda shell.bash hook)"

projname=$(basename "$PWD")
echo "Processing project: $projname"
# --- USER CUSTOMIZATION STARTS HERE ---

# Change to the LSLAutoBIDS project directory
cd ~/Documents/LSLAutoBIDS &&

# Activate the conda environment
# Make sure to replace 'autobids-new' with the name of your conda environment
conda activate autobids-new &&

# Run the main AutoBIDS script with the project name as input

python lsl_autobids/main.py -p "$projname"

# --- USER CUSTOMIZATION ENDS HERE ---
