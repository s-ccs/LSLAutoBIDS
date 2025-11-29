import os
import sys
import pytest
import yaml
import shutil
#import lslautobids
import importlib
#import lslautobids.main
# Compute project root (two levels up from current test.py)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from path_config import get_root_paths
#from test_utils.path_config import DummyCLIArgs
# Print test file name for traceability
test_file_name = os.path.basename(__file__)
print(f" Running tests in {test_file_name}")




@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_process_main_functionality(setup_project, monkeypatch):
    """
    Expect the main pipeline to raise RuntimeError when duplicate files are found.
    """
    project_name = setup_project
    paths = get_root_paths(__file__)
    print("ZZZ - main functionality")

    print(paths)


    #importlib.reload(lslautobids.config_globals)
    #importlib.reload(lslautobids.main)

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
    
    #lslautobids.config_globals.project_root = paths["project_root"]
    #lslautobids.config_globals.bids_root = paths["bids_root"]
    #lslautobids.config_globals.project_other_root = paths["project_other_root"]
    #project_toml_path = os.path.join(paths["project_root"], project_name, f"{project_name}_config.toml")

    # Reset sys.argv to something that lslautobids.main.main() expects
    sys.argv = [
        "lslautobids.main",
        "-p", project_name,
        # other args expected by lslautobids.main.main
    ]

#    dummy_cli_args = DummyCLIArgs()
#    monkeypatch.setattr("lslautobids.config_globals.cli_args", dummy_cli_args)

    # Import and run main pipeline, expect a RuntimeError
    
    import lslautobids.main

    #with pytest.raises(SystemExit, match="Duplicate file detected. Please check the file manually."):
    lslautobids.main.main()
    
    # add a subject
    shutil.copytree(os.path.join(paths["project_root"], "copy_later","sub-100"), os.path.join(paths["project_root"], project_name,"sub-100"))
    
    lslautobids.main.main()

    # cleanup
    shutil.rmtree(os.path.join(paths["project_root"], project_name,"sub-100"))
    shutil.rmtree(paths["bids_root"])


