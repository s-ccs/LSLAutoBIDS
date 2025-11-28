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