## CLI Module (`cli.py`)

The `lslautobids` command-line interface provides the main entry point for the application:

- **Commands**: `gen-proj-config`, `run`, `gen-dv-config`, `help`
- **Module mapping**: Maps commands to their respective modules
- **Argument handling**: Processes and forwards command-line arguments

#### Key Points

1. `lslautobids gen-proj-config` and `lslautobids gen-dv-config` commands generate configuration files for the project and Dataverse, respectively. This allows users to set up their project and Dataverse connection details easily before running the conversion and upload process
2. The `lslautobids run` command executes the main conversion and upload process, using the configurations generated earlier. This command runs the entire pipeline from reading XDF files, converting them to BIDS format, integrating with DataLad, and uploading to Dataverse.
3. The `lslautobids help` command provides usage information for the CLI, listing available commands and their descriptions.
