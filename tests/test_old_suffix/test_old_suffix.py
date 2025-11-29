import os
import sys
import pytest
import yaml


import importlib
# Compute project root (two levels up from current test.py)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from path_config import get_root_paths,monkeypatch_paths
#from test_utils.path_config import DummyCLIArgs

# Print test file name for traceability
test_file_name = os.path.basename(__file__)
print(f" Running tests in {test_file_name}")



@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_process_new_files_with_old_suffix(setup_project, monkeypatch):
    """
    Expect the main pipeline to raise RuntimeError when duplicate files are found.
    """
    project_name = setup_project
    paths = get_root_paths(__file__)

    monkeypatch_paths(monkeypatch,paths)

    # Reset sys.argv to something that lslautobids.main.main() expects
    sys.argv = [
        "lslautobids.main",
        "-p", project_name,
        # other args expected by lslautobids.main.main
    ]

    
    import lslautobids.main
    
    # Import and run main pipeline, expect a RuntimeError
    with pytest.raises(SystemExit, match="Duplicate file detected. Please check the file manually."):
        lslautobids.main.main()



