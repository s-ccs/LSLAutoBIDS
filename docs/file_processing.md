### File Processing Pipeline (`processing_new_files.py`)

The file processing part of the pipeline handles finding and processing new XDF files in the specified project directory:

The pipeline ensures that all newly added data files are:

1. Detected since the last run.

2. Filtered based on ignored subjects and tasks (these are specified in the project configuration file).

3. Validated against duplicate or malformed filenames.

4. Registered in the project configuration file (e.g., tasks ,etc.).

5. Converted to BIDS format and uploaded, based on user confirmation or auto-run flags.

#### 1. Detection of New Files (`check_for_new_data()`)

- Entry point of the script (from `main.py`).

- Reads project configuration (<project_name>_config.toml) to identify ignored subjects and excluded tasks (which we don't want to process and include in the BIDS dataset).

- Calls `check_for_new_files()` to scan the project directory for files modified after the last recorded run.

#### 2. Filtering (`check_for_new_files()`)

- Uses `last_run_log.txt` to determine which files are new since the last check.

- Excludes:

    - Ignored subjects (defined in the project TOML config).

    - Ignored tasks (tasks explicitly excluded in the project TOML config).

- Returns a list of candidate `.xdf` files to process or outputs a message if no new files are found and exits.

#### 3. Validation and Preparation – (`process_new_files()`)

For each new file:

- File type check: Only .xdf files are considered.

- Duplicate prevention: Files with a _old suffix (e.g., sub-001_ses-01_task-Default_old.xdf) are flagged as duplicates. The pipeline logs an error and halts execution to avoid accidental overwrites. This is currently a specific duplicate check for LSL recordings. We shall extend this in future versions.

- Task extraction: Task names are parsed from filenames (e.g., sub-888_ses-001_task-Default_run-001_eeg.xdf → task = Default).

- Configuration update: Newly discovered tasks are appended to the TOML config under [Tasks.tasks].

#### 4. User Prompt & Conversion

- If cli_args.yes is set (as a flag while running `lslautobids run`), the pipeline skips user interaction and proceeds directly to conversion. In general, this flag sets all the user prompts throughout the pipeline to 'yes', allowing for fully automated runs. 
- Otherwise, the user is prompted to confirm whether BIDS conversion should start.

- If declined, the process halts with a warning.

#### 5. BIDS Conversion and Upload (`bids_process_and_upload()`)

- Invoked only if the user confirms (or auto-run flag is set).

- Handles BIDS formatting and uploading of the processed files.

#### 6. Supporting Utility

- `_clear_last_run_log()` :Clears the last run timestamp (last_run_log.txt) when --redo_bids_conversion is specified (as a flag in `lslautobids run`), forcing reprocessing of all files.
