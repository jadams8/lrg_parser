"""Tests for lrg_parser

### Project test checklist
test_LRG_input - Reads LRG XML file as a string?
test_LRG_web_input - Gets *accurate* LRG data from internet as a string?
test_set_root - Turns LRG XML data into xml.Elemtree root object for parsing?
test_extract - Gets exon regions from root? Compare output of lrg_parse with test data.
test_convert - Converts exon regions to coordinates? Compare output of conver_coords with test data.
test_write - Assert that function uses python write function
test_BED - Assert that output file is in BED format (tab-delimited records). Use test data.
"""

import os
import lrg_parser

