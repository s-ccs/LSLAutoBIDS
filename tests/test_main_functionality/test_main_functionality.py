import os
import sys
import pytest
#import yaml
import shutil
#import lslautobids
#import importlib
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
def test_process_main_functionality(setup_project, monkeypatch):
    """
    This should not raise any errors at all!
    """
    project_name = setup_project # fixture via pytest
    paths = get_root_paths(__file__)

    monkeypatch_paths(monkeypatch,paths)
    
    from lslautobids.config_logger import get_logger
    logger = get_logger(project_name)
    logger.debug(f" Starting test_process_main_functionality in {project_name} ") 
    
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

    # sub-099 exists, but not sub-100
    fixture_path = os.path.join(paths["bids_root"],project_name,"sub-099","ses-001","eeg","sub-099_ses-001_task-freeviewing_run-2_eeg.set")
    assert os.path.exists(fixture_path)

    fixture_path = os.path.join(paths["bids_root"],project_name,"sub-100","ses-001","eeg","sub-100_ses-001_task-freeviewing_run-2_eeg.set")
    assert not os.path.exists(fixture_path)
    # add a subject
    shutil.copytree(os.path.join(paths["project_root"], "copy_later","sub-100"), os.path.join(paths["project_root"], project_name,"sub-100"))
    
    lslautobids.main.main()

    # test that bids/sub-100 folder exists
    # test that both subjects have experiment.tar.gz with identical content

    fixture_path = os.path.join(paths["bids_root"],project_name,"sub-100","ses-001","eeg","sub-100_ses-001_task-freeviewing_run-2_eeg.set")
    assert os.path.exists(fixture_path)

    # cleanup 
    shutil.rmtree(os.path.join(paths["project_root"], project_name,"sub-100"))

    # # does not work for some reason with git-annex, needs sudo
    #shutil.rmtree(paths["bids_root"])


