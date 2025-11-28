import os
import subprocess
import sys

# --- Setup ---
BASE_DIR = os.path.dirname(__file__) # base tests directory
TESTCASES_DIR = os.path.join(BASE_DIR, "testcases")
TEST_UTILS_DIR = os.path.join(BASE_DIR, "test_utils")

# Make both testcases and test_utils importable
sys.path.insert(0, TESTCASES_DIR)
sys.path.insert(0, TEST_UTILS_DIR)


print("Searching for test directories...\n")

for folder in os.listdir(TESTCASES_DIR):
    folder_path = os.path.join(TESTCASES_DIR, folder)

    if (
        folder.startswith("test_")
        and os.path.isdir(folder_path)
        and any(f.endswith(".py") for f in os.listdir(folder_path))
        and os.path.exists(os.path.join(folder_path, "data"))
    ):
        print(f"Running tests in: {folder} which has folder path {folder_path}")
        subprocess.run(["pytest", folder_path])
    else:
        print(f"Skipping: {folder} (no tests file or data). Recheck if the test files are in place or data folder is missing.")
