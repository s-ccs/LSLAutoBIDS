### Other Utility Modules

#### 1. Global Configuration Management (`config_globals.py`)
This module manages global configuration settings and command-line arguments using a singleton pattern. The `CLIArgs` class ensures that there is only one instance of the configuration throughout the application. It provides methods to parse and retrieve command-line arguments and global configuration settings (lslautobids_config.yaml), which are then used across various modules.

#### 2. Logging Configuration (`config_logger.py`)
This module sets up a global logger for the application. The `get_logger()` function creates and configures a logger instance with a specified project name. It ensures that all log messages are formatted consistently and that log levels are set appropriately. The final log file is stored in the `<BIDS_ROOT>/<project-name>/code/` folder of the BIDS dataset.

The log file is also available as a part of the created dataset.

#### 3. Utility Functions (`utils.py`)
This module contains various utility functions used across the application. 
1. `get_user_input` : Handles user prompts and input validation. This function allows five attempts for valid input before exiting. The function takes the user prompt message as an argument and returns the user input.
2. `read_toml_file` : Reads and parses a TOML file, returning its contents as a dictionary.
3. `write_toml_file` : Writes a dictionary to a TOML file.