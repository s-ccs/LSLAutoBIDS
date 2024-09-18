import datalad.api as dl
import os


def create_and_add_files_to_datalad_dataset(dataset_path,flag):
    if flag==0:
        # Create a new dataset
        print('Creating a new datalad dataset........')
        dl.create(dataset_path, force=True)
    # Commit changes
    # Change to dataset path
    os.chdir(dataset_path)
    with open(os.path.join(dataset_path,".gitattributes"), "a") as f:
        f.write("* annex.largefiles=nothing")
    print('Committing current changes........')
    dl.save(path = '.', message="First BIDS upload test")
    
