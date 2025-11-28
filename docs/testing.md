## Testing

The testing framework uses `pytest` to validate the functionality of the core components.

- The tests are located in the `tests/` directory and cover various modules including configuration generation, file processing, BIDS conversion, DataLad integration, and Dataverse interaction. (Work in progress)

- The test directory contains :
    - `test_utils` : Directory containing utility functions needed across multiple test files.
    - `testcases` : Directory containing all the tests in a in a directory structure - `test_<test_name>`.
    - Each `test_<test_name>` directory contains a `data` folder with sample data for that test and a `test_<test_name>.py` file with the actual test cases.
    - `run_all_tests.py` : A script to run all the tests in the `testcases` directory sequentially.

Tests will be added continuously as new features are added and existing features are updated.

### Running Tests

To run the tests, we recommend to use `uv run pytest` (caveat, for some reason somtimes tests fail if they are all run at the same time. you can then run them via `uv run pytest tests/testcase/test_main_functionality` and they will work).

These tests ensure that each component functions as expected and that the overall pipeline works seamlessly. This tests will also be triggered automatically on each push or PR to the main repository using GitHub Actions.