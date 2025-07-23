#!/bin/bash
eval "$(conda shell.bash hook)"

projname=$(basename "$PWD")
echo "Processing project: $projname"
# --- USER CUSTOMIZATION STARTS HERE ---

cd ~/Documents/LSLAutoBIDS &&

	conda activate autobids-new &&
python lslautobids/main.py -p $projname

# --- USER CUSTOMIZATION ENDS HERE ---
