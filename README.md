# Github Issue handler

## Installation
After cloning the repo, make it the working directory, create a virtual environment 
and run:
```bash
$ pip install -r requirements.txt
```
Note: Python >= 3.10 is required.

## Usage
It is recommended to run this module from the directory containing the `setup.py` file, 
since the PDFs and Chrome user profile will be created from wherever you invoke the script.
```bash
$ python3 -m issuehandler.issuehandler [CLI options...]
```
or
```bash
$ python3 -m issuehandler.batchrunner [CLI options...]
```