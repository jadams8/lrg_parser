"""Tests for lrg_parser"""
import os, subprocess, difflib, time
import xml.etree.ElementTree as ET
import pytest
import requests
import lrg_parser

# test_convert - Converts exon regions to coordinates? Compare output of conver_coords with test data.NM
# test_write - Assert that function uses python write function JA
# test_BED - Assert that output file is in BED format (tab-delimited records). Use test data. NM

def test_parse_lrg1():
    """Test that all expected exon labels are parsed from LRG files."""
    # Get exons for LRG 1
    lrg1_root = lrg_parser.set_root(lrg_parser.parse_file('data/LRG_1.xml'))
    lrg1_exon_data_tuple = (lrg_parser.lrg_parse(lrg1_root))
    # Exon labels are the first element of each tuple in lrg1_exon_data_tupe. zip() is used to 
    # collec the exons from the first elements. e.g.:
    #     a = [(1,2,3), (4,5,6)]
    #     zip(*a) = [(1,4), (2,5), (3,6)]
    lrg1_exons = list(zip(*lrg1_exon_data_tuple))[0]
    # Get exon label truthset from local data
    lrg1_truthset = open('data/LRG1_exons.list', 'r').read().split(",")
    assert set(lrg1_exons) == set(lrg1_truthset)

def test_parse_lrg5():
    """Test that all expected exon labels are parsed from LRG files."""
    # Get exons for LRG 5
    lrg5_root = lrg_parser.set_root(lrg_parser.parse_file('data/LRG_5.xml'))
    lrg5_exon_data_tuple = (lrg_parser.lrg_parse(lrg5_root))
    lrg5_exons = list(zip(*lrg5_exon_data_tuple))[0]
    # Get exon label truthset from local data
    lrg5_truthset = open('data/LRG5_exons.list', 'r').read().split(",")
    assert set(lrg5_exons) == set(lrg5_truthset)

def test_write():
    """Test that it writes a file with the correct name """
    # write_file function writes the data to a file
    lrg_parser.write_file('data', 'LRG_1.xml')
    # Test that a file was output with the correct name (LRG_num_date.bed)
    date_today = time.strftime('%Y%m%d')
    assert os.path.isfile('LRG_1_'+date_today+'.bed')
    os.remove('LRG_1_'+date_today+'.bed')

# This test requires the user to take additional measures to ensure it
# passes and is therefore not an appropriate test. It is not possible
# to ensure the content of files are exactly the same as the content
# automatically changes depending on the date of access.
#
# def test_LRG_web_input():
#     """Test that the text in the file downloaded using the script is the
#     same as the information in an XML file downloaded manually N.B. XML
#     file MUST be manually downloaded on the same day as this test is run"""
#     # open file downloaded manually and stored in 'data' directory
#     with open('data/LRG_1.xml', 'r') as file_1:
#         f1 = file_1.read()
#     # get file gets the xml data from the web as a string
#     f2 = lrg_parser.get_file('LRG_1')
#     # test that the manually downloaded and automatically downloaded
#     # strings are identical
#     assert f1 == f2

# Best way to check the content matches is to check that both strings
# are the same length, rather than being identical.

def test_length():
    """Test that the automatically downloaded XML using the script
    and a manually downloaded XML for the same LRG are the same 
    length. We assume it is unlikely that different LRG files will
    be exactly the same length"""
    # open file downloaded manually, stored in 'data' directory
    with open('data/LRG_1.xml', 'r') as file_1:
        f1 = file_1.read()
    # get_file gets the xml data from web as a string
    f2 = lrg_parser.get_file('LRG_1')
    # check that the strings are exactly the same length
    assert len(f1) == len(f2)

def test_LRG_input():
    """Test that if the input is an existing file, parse_file outputs
    it as a string"""
    data = lrg_parser.parse_file('data/LRG_1.xml')
    assert isinstance(data, str)

def test_set_root_from_file():
    """Test that the xml data string objects are converted to root 
    objects for parsing for file inputs"""
    root = lrg_parser.set_root(lrg_parser.parse_file('data/LRG_1.xml'))
    assert isinstance(root, ET.Element)

def test_set_root_from_name():
    """Test that the xml data string objects are converted to root 
    objects for parsing for LRG number inputs"""
    root = lrg_parser.set_root(lrg_parser.get_file('LRG_1'))
    assert isinstance(root, ET.Element)