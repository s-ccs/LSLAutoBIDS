import os
# Set up the BIDS output path
BIDS_ROOT = '../data/bids/'

# This is the actual path to the directory containing xdf files
PROJECT_ROOT = '../data/projects/'

# This is the actual path to the directory containing the stimulus files
PROJECTS_STIM_ROOT = '../data/project_stimulus/'

def list_directories(path=PROJECT_ROOT):
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories

PROJECTS = list_directories(PROJECT_ROOT)
