import datalad.api as dl
import os


def create_and_add_files_to_datalad_dataset(dataset_path,flag):
    message = "LSL Auto BIDS: new files found and added"
    if flag==0:
        message ="LSL Auto BIDS: new datalad dataset created"
        # Create a new dataset
        print('Creating a new datalad dataset........')
        dl.create(dataset_path, force=True)
    # Commit changes
    # Change to dataset path
    os.chdir(dataset_path)
    if flag==0:
    	# needed to modify participants.tsv etc. later
    	with open(os.path.join(dataset_path,".gitattributes"), "a") as f:
            f.write("* annex.largefiles=nothing")
    print('Committing current changes........')
    dl.save(path = '.', message=message)
    
