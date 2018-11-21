import lrg_parser
import os

def test_creates_file():
    '''Test that it creates a new file from an XML input'''
    lrg_parser.lrg_parse('data/LRG_1.xml')
    assert os.path.isfile('lrg1.txt')
