import xml.etree.ElementTree as ET
import os, argparse


def lrg_parse(xml_file):
	"""function will parse the LRG file to extract the exon number and LRG co-ordinates for the start and end of each codon"""
	lrg1 = ET.parse(xml_file)
	# set root as reference to read the rest of the XML file
	root = lrg1.getroot()
	# create the empty list to store the output
	data_list = []
	# iterate through each exon in the LRG
	for exon in root.iter('exon'):
		# ensure that the exon has a label so it is part of the transcript
		if 'label' in exon.attrib.keys():
			for child in exon:
				# make sure the only co-ordinates printed are the LRG co-ordinates
				if 'LRG_1' in child.attrib.values():
					data_list.append([exon.attrib['label'], child.attrib['start'], child.attrib['end']])
	return data_list

def main():
	parser = argparse.ArgumentParser(description='Parse an XML file to produce a BED file')
	parser.add_argument('xml_file', help='Enter the name of the LRG file to parse')
	args = parser.parse_args()

	# store the output from lrg_parse() in a variable to write to a file
	data = lrg_parse(args.xml_file) 

	file_name = args.xml_file.split('.')[0]+'.bed'

	with open(file_name, 'w') as myfile:
		for my_list in data:
			# reformat the list to tab seperated and different lines
			new_list = "\t".join(my_list) + '\n'
			myfile.write(new_list)

if __name__ == "__main__":
	main()