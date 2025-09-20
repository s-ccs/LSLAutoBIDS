import os
import sys
import pytest
import yaml


# Compute project root (two levels up from current test.py)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from test_utils.path_config import get_root_paths

# Print test file name for traceability
test_file_name = os.path.basename(__file__)
print(f" Running tests in {test_file_name}")

# Dummy CLI argument simulation
class DummyCLIArgs:
    def __init__(self):
        self.project_name = "test-project"
        self.yes = True
        self.redo_bids_conversion = False 
        self.redo_other_pc = False   
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
    os.makedirs(paths["project_root"], exist_ok=True)

    from lslautobids.gen_project_config import main as gen_project_config_main

    # Create dummy user config for the test
    config_file_test = os.path.join(os.path.expanduser("~"),'.config/lslautobids/test-autobids_config.yaml')
    os.makedirs(os.path.dirname(config_file_test), exist_ok=True)
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
    monkeypatch.setattr("lslautobids.config_globals.cli_args", dummy_cli_args)
    monkeypatch.setattr("lslautobids.config_globals.config_file", config_file_test)

    # Simulate CLI call to generate config
    monkeypatch.setattr(sys, "argv", [
        "gen_project_config.py",
        "-p", project_name,
        "-c", config_file_test
    ])

    gen_project_config_main()

    return paths, project_name 


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_process_new_files_with_old_suffix(setup_project, monkeypatch):
    """
    Expect the main pipeline to raise RuntimeError when duplicate files are found.
    """
    paths, project_name = setup_project

    project_toml_path = os.path.join(paths["project_root"], project_name, f"{project_name}_config.toml")

    # Reset sys.argv to something that lslautobids.main.main() expects
    sys.argv = [
        "lslautobids.main",
        "-p", project_name,
        # other args expected by lslautobids.main.main
    ]

    dummy_cli_args = DummyCLIArgs()
    monkeypatch.setattr("lslautobids.config_globals.cli_args", dummy_cli_args)

    # Import and run main pipeline, expect a RuntimeError
    from lslautobids.main import main as runlslautobids
    with pytest.raises(SystemExit, match="Duplicate file detected. Please check the file manually."):
        runlslautobids()



