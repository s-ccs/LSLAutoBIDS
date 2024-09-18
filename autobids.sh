#!/bin/bash
eval "$(conda shell.bash hook)"

projname=$(basename "$PWD")
echo "Processing $projname"
cd ~/Documents/LSLAutoBIDS&&

	conda activate autobids-new &&
python lsl_autobids/main.py -p $projname

