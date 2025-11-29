import pytest
import sys,os
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
import yaml

from path_config import get_root_paths


# Dummy CLI argument simulation
class DummyCLIArgs:
    def __init__(self):
        self.project_name = "test-project"
        self.yes = True
        self.redo_bids_conversion = False 
        self.redo_other_pc = False   
        self.push_to_dataverse = False
    def init(self, args):
        # you can store the args or ignore
        pass

@pytest.fixture(scope="function")
def setup_project(monkeypatch):
    """
    Setup test environment, patch config paths and simulate CLI behavior.
    """
    paths = get_root_paths(__file__)
    
    dummy_cli_args = DummyCLIArgs()
    project_name = dummy_cli_args.project_name

    # Ensure directory exists
    #os.makedirs(paths["project_root"], exist_ok=True)

    from lslautobids.gen_project_config import main as gen_project_config_main

    # Create dummy user config for the test
    #config_file_test = os.path.join(os.path.expanduser("~"),'.config/lslautobids/test-autobids_config.yaml')
    config_file_test = ("tests/pytest-autobids_config.yaml")
    
    #os.makedirs(os.path.dirname(config_file_test), exist_ok=True)
    config_data = {
        "PROJECT_ROOT": paths["project_root"],
        "BIDS_ROOT": paths["bids_root"],
        "PROJECT_OTHER_ROOT": paths["project_other_root"],
    }
    
    with open(config_file_test, "w") as f:
        yaml.dump(config_data, f)

    print("Config YAML written.")
    
    # Patch global paths and CLI args
    monkeypatch.setattr("lslautobids.config_globals.project_root", paths["project_root"])
    monkeypatch.setattr("lslautobids.config_globals.bids_root", paths["bids_root"])
    monkeypatch.setattr("lslautobids.config_globals.project_other_root", paths["project_other_root"])
    monkeypatch.setattr("lslautobids.config_globals.dataverse_base_url","https://demodarus.izus.uni-stuttgart.de/")
    monkeypatch.setattr("lslautobids.config_globals.api_key","8b6c479e-e85b-4edb-9b8a-5305a9976875")
    monkeypatch.setattr("lslautobids.config_globals.parent_dataverse_name","s-ccs")
    #monkeypatch.setattr("lslautobids.config_globals.parent_dataverse_name","Institute for Visualization and Interactive Systems")
    monkeypatch.setattr("lslautobids.config_globals.cli_args", dummy_cli_args)
    monkeypatch.setattr("lslautobids.config_globals.config_file", config_file_test)

    # Simulate CLI call to generate config
    monkeypatch.setattr(sys, "argv", [
        "gen_project_config.py",
        "-p", project_name,
        "-c", config_file_test
    ])

    gen_project_config_main()

    yield project_name 

    # crashdown
    #os.remove(config_file_test)