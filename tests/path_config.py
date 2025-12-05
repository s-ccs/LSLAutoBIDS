import os

def get_root_paths(test_file: str):
    """
    Given a test file (__file__), return relevant test root paths.
    """
    # Use the test_file argument, not __file__ from path_config.py
    test_folder = os.path.basename(os.path.dirname(test_file))

    # Go up to the test folder's path and into its `data/` directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(test_file), "data"))

    print(f'The base dir in the get_roots_path function is "{base_dir}"')
    return {
        "project_root": os.path.join(base_dir, "projects"),
        "bids_root": os.path.join(base_dir, "bids"),
        "project_other_root": os.path.join(base_dir, "project_other"),
    }



def monkeypatch_paths(monkeypatch,paths):
    monkeypatch.setattr("lslautobids.config_globals.project_root", paths["project_root"])
    monkeypatch.setattr("lslautobids.convert_to_bids_and_upload.project_root", paths["project_root"])
    monkeypatch.setattr("lslautobids.generate_dataset_json.project_root", paths["project_root"])
    monkeypatch.setattr("lslautobids.main.project_root", paths["project_root"])
    monkeypatch.setattr("lslautobids.processing_new_files.project_root", paths["project_root"])

    monkeypatch.setattr("lslautobids.config_globals.bids_root", paths["bids_root"])
    monkeypatch.setattr("lslautobids.convert_to_bids_and_upload.bids_root", paths["bids_root"])
    monkeypatch.setattr("lslautobids.main.bids_root", paths["bids_root"])
    
    monkeypatch.setattr("lslautobids.config_logger.bids_root", paths["bids_root"])
    monkeypatch.setattr("lslautobids.config_globals.project_other_root", paths["project_other_root"])
    monkeypatch.setattr("lslautobids.convert_to_bids_and_upload.project_other_root", paths["project_other_root"])
    #monkeypatch.setattr("lslautobids.config_logger._logger",None)
    
    