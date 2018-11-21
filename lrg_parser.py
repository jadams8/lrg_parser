import xml.etree.ElementTree as ET
import os

def lrg_parse(file_name):
	"""function will parse the LRG file to extract the exon number and LRG co-ordinates for the start and end of each codon"""
	lrg1 = ET.parse(file_name)
	root = lrg1.getroot() # set root as reference to read the rest of the XML file
	data_list = [] # create the empty list to store the output
	for exon in root.iter('exon'): # iterate through each exon in the LRG
		if 'label' in exon.attrib.keys(): # ensure that the exon has a label so it is part of the transcript
			for child in exon:
				if 'LRG_1' in child.attrib.values(): # make sure the only co-ordinates printed are the LRG co-ordinates
					data_list.append([exon.attrib['label'], child.attrib['start'], child.attrib['end']])
	return data_list

data = lrg_parse('data/LRG_1.xml') # store the output from lrg_parse() in a variable to write to a file

with open('lrg1.txt', 'w') as myfile:
	for my_list in data:
		new_list = "\t".join(my_list) + '\n' #reformat the list to tab seperated and different lines
		print(new_list)
		myfile.write(new_list)
