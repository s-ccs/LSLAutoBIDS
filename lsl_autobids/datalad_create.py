import datalad.api as dl
from .folder_config import BIDS_ROOT

def create_and_add_files_to_dataset(dataset_path):
    # Create a new dataset
    dl.create(dataset_path, force=True)

    # Commit changes
    dl.save(dataset_path, message="First BIDS upload test")

def main():
    dataset_path = BIDS_ROOT
    create_and_add_files_to_dataset(dataset_path)

if __name__ == "__main__":
    main()