import xml.etree.ElementTree as ET
import os, argparse, fnmatch, re


def lrg_parse(xml_file):
	"""function will parse the LRG file to extract the exon number and LRG co-ordinates for the start and end of each codon"""
	lrg = ET.parse(xml_file)
	# set root as reference to read the rest of the XML file
	root = lrg.getroot()
	# create the empty list to store the output
	data_list = []
	# iterate through each exon in the LRG
	for exon in root.iter('exon'):
		# ensure that the exon has a label so it is part of the transcript
		if 'label' in exon.attrib.keys():
			for child in exon:
				# make sure the only co-ordinates printed are the LRG co-ordinates
				if fnmatch.filter(child.attrib.values(), 'LRG_?'):
					data_to_append = (exon.attrib['label'], child.attrib['start'], child.attrib['end'])
					if data_to_append not in data_list:
						data_list.append(data_to_append)
	sorted_data = sorted(data_list, key=lambda line: int(re.split('[A-Za-z]+', line[0])[0]))
	return sorted_data


def main():
	parser = argparse.ArgumentParser(description='Parse an XML file to produce a BED file')
	parser.add_argument('xml_file', help='Enter the name of the LRG file to parse')
	args = parser.parse_args()

	# store the output from lrg_parse() in a variable to write to a file
	data = lrg_parse(args.xml_file)

	file_name = args.xml_file.split('.')[0]+'.bed'

	with open(file_name, 'w') as myfile:
		for my_tuple in data:
			# reformat the list to tab seperated and different lines
			my_list = "\t".join(my_tuple) + '\n'
			myfile.write(my_list)

if __name__ == "__main__":
	main()