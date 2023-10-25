import datalad.api as dl


def create_and_add_files_to_dataset(dataset_path,flag):
    if flag==0:
        # Create a new dataset
        print('Creating a new datalad dataset........')
        dl.create(dataset_path, force=True)
    # Commit changes
    print('Committing current changes........')
    dl.save(dataset_path, message="First BIDS upload test")

