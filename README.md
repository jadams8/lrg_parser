# lrg_parser v1.0
*Created by: Jes Adams (jadams8) and Nana Mensah (nmns93)*

## About
Generate BED file from LRG XML files using exon coordinates. Two inputs are accepted by the script in any combination:
* LRG files in XML format.
* An LRG number, e.g. `LRG_5`. XML files are retrieved from the API for these inputs.

Documentation for the methods were generated with `pydoc`. These are available in docs/lrg_parser.txt

## Dependencies
The script relies on the third-party `requests` module. It has been tested with python version 3.6.

## Usage
```
lrg_parser.py [-h] xml_file [xml_file ...]

Parse an XML file to produce a BED file

positional arguments:
  xml_file    Enter the names of the LRG file to parse

optional arguments:
  -h, --help  show this help message and exit
```
