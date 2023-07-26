import datalad.api as dl

import datalad.api as dl

def create_and_add_files_to_dataset(dataset_path):
    # Create a new dataset
    dl.create(dataset_path, force=True)

    # Commit changes
    dl.save(dataset_path, message="Added dummy.txt file")

if __name__ == "__main__":
    dataset_path = './test_data'
    create_and_add_files_to_dataset(dataset_path)