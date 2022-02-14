# Github Issue handler

## Installation
After cloning the repo, make it the working directory, create a virtual environment 
and run:
```bash
$ pip install -r requirements.txt
```
**Note:** `Python >= 3.10` is required.

## Usage
You can run this module from any directory, but note that the PDF files
will be saved to the current directory in `./pdfs/` 
```bash
$ python3 -m issuehandler.issuehandler [CLI options...]
```
or
```bash
$ python3 -m issuehandler.batchrunner [CLI options...]
```