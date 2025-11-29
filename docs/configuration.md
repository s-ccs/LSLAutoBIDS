## Configuration System

The configuration system manages dataversse and project-specific settings using YAML and TOML files.

#### Dataverse and Project Root Configuration (`gen_dv_config.py`)

This module generates a global configuration file for Dataverse and project root directories. This is a one-time setup per system.  This file is stored in `~/.config/lslautobids/autobids_config.yaml` and contains:
- Paths for BIDS, projects, and project_other directories : This allows users to specify where their eeg data, behavioral data, and converted BIDS data are stored on their system. This paths should be relative to the home/users directory of your system and string format.

- Dataverse connection details: Base URL, API key, and parent dataverse name for uploading datasets. Base URL is the URL of the dataverse server (e.g. https://darus.uni-stuttgart.de), API key is your personal API token for authentication (found in your dataverse account settings), and parent dataverse name is the name of the dataverse under which datasets will be created (this can be found in the URL when you are in the dataverses page just after 'dataverse/'). For example, if the URL is `https://darus.uni-stuttgart.de/dataverse/simtech_pn7_computational_cognitive_science`, then the parent dataverse name is `simtech_pn7_computational_cognitive_science`.

**Commands and arguments**

The command to generate the dataverse configuration file is:
```
lslautobids gen-dv-config
```
_Currently, the package doesn't allow you to have multiple dataverse configurations. This will be added in future versions and can be easily adapted_

#### Project Configuration (`gen_project_config.py`)
This module generates a project-specific configuration file in TOML format. This file is stored in the `projects/<PROJECT_NAME>/<PROJECT_NAME>_config.toml` file and contains:
- Project metadata: Title, description, license, and authors, etc.

**Commands and arguments**

The command to generate the project configuration file is:
```
lslautobids gen-proj-config --project <projectname>  
```
- `--project <projectname>`: Specifies the name of the project for which the configuration file is to be generated. This argument is *required*.
- `--standalone_toml` : (Optional) If provided, the generated configuration file will be a standalone TOML file in the current directory, without being placed in the project directory.
- `--custom_dv_config` : (Optional) Path to a custom YAML configuration file (dataverse and project root configuration) for Dataverse and project root directories. If not provided, the default path `~/.config/lslautobids/autobids_config.yaml` will be used. This is specified to allow flexibility in using different configurations for different projects or testing purposes.