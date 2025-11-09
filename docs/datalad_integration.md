### 4. DataLad Integration (`datalad_create.py`)

The DataLad integration module manages the creation and updating of DataLad datasets for version control of the BIDS dataset. This function initializes a DataLad dataset at a given project path.
The function performs the following steps:
1. Initialize commit message. It first sets a initialization message : "LSL Auto BIDS: new files found and added".
2. If flag == 0 (new dataset), the message is overwritten with "LSL Auto BIDS: new datalad dataset created".
3. Further, if flag == 0 we try to create a new DataLad dataset in the specified path (dataset_path) using `dl.create()`. This is similar to running `datalad create` from the command line for datalad CLI or `git init` for git CLI. This function is executed using :

`dl.create(dataset_path, force=True)`

Here, since the directory may already contain files (BIDS directory in our case), we use force=True to allow creation of the dataset even if files already exist and it is not an empty directory.

4. If it raises an exception (e.g., if the path is not a directory or if DataLad already exists ), it logs an error and exits the program.

5. This function also changes the current working directory to the dataset_path using `os.chdir(dataset_path)` so subsequent DataLad operations (like `datalad save`, `datalad push`) run in the context of this dataset.

6. This function also manages the .gitattributes file to ensure that large files are handled by git-annex and small text/metadata files are handled by git. This is done by appending specific patterns to the .gitattributes file. For example:
`*.csv annex.largefiles=nothing` means .csv files are treated as small files and stored directly in git. Similarly, *    annex.largefiles=largerthan=100kb` means files larger than 100kb are managed by git-annex.

7. Finally, it saves the changes to the DataLad dataset using `dl.save()` with the appropriate commit message. This save command stages all changes (new files, modified files) and commits them to the DataLad dataset.

8. If flag!=0 (existing dataset), it skips the initialization step and directly saves any new changes to the existing DataLad dataset.
