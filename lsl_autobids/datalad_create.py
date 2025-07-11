import datalad.api as dl
import os


def create_and_add_files_to_datalad_dataset(dataset_path,flag, logger):
    message = "LSL Auto BIDS: new files found and added"
    if flag==0:
        message ="LSL Auto BIDS: new datalad dataset created"
        # Create a new dataset
        logger.info('Creating a new datalad dataset........')
        try:
            dl.create(dataset_path, force=True) # files already exist, so we eforce it
        except:
            logger.info("Could not create a new dataset, maybe it exists already?")

    # Commit changes
    # Change to dataset path
    os.chdir(dataset_path)
    if flag==0:
    	# needed to modify participants.tsv etc. later
    	with open(os.path.join(dataset_path,".gitattributes"), "a") as f:
            f.write("* annex.largefiles=largerthan=100kb")
            f.write("\n*.csv annex.largefiles=nothing")
            f.write("\n*.tsv annex.largefiles=nothing")
            f.write("\n*.md annex.largefiles=nothing")
            f.write("\n*.json annex.largefiles=nothing")
    logger.info('Committing current changes........')
    dl.save(path = '.', message=message)
    
