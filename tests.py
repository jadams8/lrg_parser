"""Tests for lrg_parser"""
import os
import lrg_parser

def test_creates_file():
    '''Test that it creates a new file from an XML input'''
    # Call from command line 
    lrg_parser.lrg_parse('data/LRG_1.xml')
    # Assert that a file was output
    assert os.path.isfile('lrg1.txt')

def test_all_exons():
    """Test all LRG_5 exon labels are present in first column of lrg_parser output"""
    # Create a list of exon labels expected in LRG_5
    exon_labels = [ str(number) for number in range(1,15) ]
    exon_labels.extend(['14a','14b','14c'])
    #lrg_parser.lrg_parse('data/LRG_5.xml')
    print(exon_labels)

