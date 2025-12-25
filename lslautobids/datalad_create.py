import datalad.api as dl
import os


def create_and_add_files_to_datalad_dataset(dataset_path,logger):
    message = "LSL Auto BIDS: new files found and added"
    #if flag==0:
    ds = dl.Dataset(dataset_path)
    if not ds.is_installed():
        message ="LSL Auto BIDS: new datalad dataset created"
        logger.info("Creating a new datalad dataset........")
        try:
            dl.create(dataset_path, force=True) # files already exist, so we eforce it

            # make sure only large files are saved
            with open(os.path.join(dataset_path,".gitattributes"), "a") as f:
                f.write("* annex.largefiles=largerthan=100kb")
                f.write("\n*.csv annex.largefiles=nothing")
                f.write("\n*.log annex.largefiles=nothing")
                f.write("\n*.tsv annex.largefiles=nothing")
                f.write("\n*.md annex.largefiles=nothing")
                f.write("\n*.json annex.largefiles=nothing")

        except Exception:
            logger.info("Could not create a new dataset, maybe it exists already?")


    # commit current files
    logger.info('Committing current changes........')
    dl.save(path = dataset_path, message=message)
    
