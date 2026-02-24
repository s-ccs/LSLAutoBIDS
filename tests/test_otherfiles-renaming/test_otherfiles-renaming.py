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


from path_config import get_root_paths,monkeypatch_paths
#from test_utils.path_config import DummyCLIArgs
# Print test file name for traceability
test_file_name = os.path.basename(__file__)
print(f" Running tests in {test_file_name}")




@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_process_otherfiles_renaming(setup_project, monkeypatch):
    """
    Expect the main pipeline to raise RuntimeError when duplicate files are found.
    """
    project_name = setup_project # fixture via pytest
    paths = get_root_paths(__file__)

    monkeypatch_paths(monkeypatch,paths)
    
    
    # Reset sys.argv to something that lslautobids.main.main() expects
    # this effectively removes the -c from setup_project
    sys.argv = [
        "lslautobids.main",
        "-p", project_name,
        # other args expected by lslautobids.main.main
    ]
    
    # run once
    import lslautobids.main
    lslautobids.main.main()

    # cleanup # doesnt work for some reason with git-annex, needs sudo
    #shutil.rmtree(paths["bids_root"])


