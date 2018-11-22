"""Tests for lrg_parser"""
import os, subprocess
import lrg_parser

def test_creates_file():
    """Test that it creates a new file from an XML input"""
    # Call from command line
    subprocess.call(['python', 'lrg_parser.py', 'data/LRG_1.xml'])
    # Assert that a file was output
    assert os.path.isfile('data/LRG_1.bed')

def test_all_exons():
    """Test all LRG_5 exon labels are present in first column of lrg_parser output"""
    # Create a list of exon labels expected in LRG_5
    exon_labels = [str(number) for number in range(1, 14)]
    exon_labels.extend(['14a', '14b', '14c', '15'])
    # Create a list of exons parsed from LRG_5
    parsed_data = lrg_parser.lrg_parse('data/LRG_5.xml')
    parsed_exons = set([item[0] for item in parsed_data])
    # Test that all expected exon labels are present
    for exon_label in exon_labels:
        assert exon_label in parsed_exons
