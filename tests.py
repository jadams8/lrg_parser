"""Tests for lrg_parser"""
import os, subprocess, difflib, time
import xml.etree.ElementTree as ET
import lrg_parser

def test_write():
    """Test that it writes a file with the correct name """
    # write_file function writes the data to a file
    lrg_parser.write_file('data', 'LRG_1.xml')
    # Test that a file was output with the correct name (LRG_num_date.bed)
    date_today = time.strftime('%Y%m%d')
    assert os.path.isfile('LRG_1_'+date_today+'.bed')

def test_LRG_web_input():
    """Test that the text in the file downloaded using the script is the
    same as the information in an XML file downloaded manually N.B. XML
    file MUST be manually downloaded on the same day as this test is run"""
    # open file downloaded manually and stored in 'data' directory
    with open('data/LRG_1.xml', 'r') as file_1:
        f1 = file_1.read()
    # get file gets the xml data from the web as a string
    f2 = lrg_parser.get_file('LRG_1')
    # test that the manually downloaded and automatically downloaded
    #strings are identical
    assert f1 == f2

def test_LRG_input():
    """Test that if the input is a """
    data = lrg_parser.parse_file('data/LRG_1.xml')
    assert isinstance(data, str)