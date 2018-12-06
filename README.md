# lrg_parser v1.0
*Created by: Jes Adams (jadams8) and Nana Mensah (nmns93)*

## About
Generate BED file from LRG XML files using exon coordinates. Two inputs are accepted by the script in any combination:
* LRG files in XML format.
* An LRG number, e.g. `LRG_5`. XML files are retrieved from the API for these inputs.

Documentation for the methods were generated with `pydoc`. These are available in docs/lrg_parser.txt

## Installation
### Unix command line
```
git clone https://github.com/jadams8/lrg_parser.git
cd lrg_parser
pip install -r requirements.txt
export PATH=$PATH:$(pwd) # Add to ~/.bashrc for access from every terminal session
```

### Testing
```
pytest lrg_parser/tests.py
```

## Dependencies
Tested with python version 3.6 only. Requires an internet connection to install dependencies listed in *requirements.txt*.

## Usage
```
lrg_parser.py [-h] xml_file [xml_file ...]

Parse an XML file to produce a BED file

positional arguments:
  xml_file    Enter the names of the LRG file to parse

optional arguments:
  -h, --help  show this help message and exit
```
