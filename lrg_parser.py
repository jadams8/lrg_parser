#!/usr/bin/env python3
'''lrg_parser.py

Parse exon regions from an LRG record in XML format to a BED file containing GRCh38 regions
'''
import xml.etree.ElementTree as ET
import os, argparse, fnmatch, re, requests, time


def parse_file(xml_file):
	'''read an input file as a string object'''
	print('file found on system')
	with open(xml_file, 'r') as input_file:
		output = input_file.read()
	return output

def lrg_parse(root):
	'''Parse an LRG file contained in an xml.etree.ElementTree object.
	Returns: A list of exon coordinates for GRCh38'''
	# create the empty list to store the output
	data_list = []
	# iterate through each exon in the LRG
	for exon in root.iter('exon'):
		# ensure that the exon has a label so it is part of the transcript
		if 'label' in exon.attrib.keys():
			for child in exon:
				# make sure the only co-ordinates printed are the LRG co-ordinates
				if list(root.iter('id'))[0].text == child.attrib['coord_system']:
					# create a list of data that needs to be in the bed file
					data_to_append = (exon.attrib['label'], child.attrib['start'], child.attrib['end'])
					# only append data that is not already in the list to prevent duplications
					if data_to_append not in data_list:
						data_list.append(data_to_append)
	# sort the data according to position in the genome
	sorted_data = sorted(data_list, key=lambda line: int(re.split('[A-Za-z]+', line[0])[0]))
	return(sorted_data)

def write_file(data, f_in):
	'''write the data from parsing into a new bed file with the same name as the XML file'''
	file_name = f_in.split('.')[0]+'_'+time.strftime('%Y%m%d')+'.bed'
	with open(file_name, 'w') as myfile:
		for my_tuple in data:
			# reformat the list to tab seperated and different lines
			my_list = "\t".join(my_tuple) + '\n'
			myfile.write(my_list)
	return file_name

def get_file(lrg_num):
	'''if the file is not already on the system get the file from the LRG website'''
	print(lrg_num + ' not found on system, retrieving from internet.')
	website = 'http://ftp.ebi.ac.uk/pub/databases/lrgex/'+ lrg_num +'.xml'
	xml_text = requests.get(website)
	# LRGs pending approval will have a different URL, so if the above web
	# address throws a 404 error then use a different URL with 'pending' in
	if xml_text.status_code == 404:
		website = 'http://ftp.ebi.ac.uk/pub/databases/lrgex/pending/'+ lrg_num +'.xml'
		xml_text = requests.get(website)
	return xml_text.text

def set_root(xml_data):
	root = ET.fromstring(xml_data)
	print('root created successfully')
	return root

def convert_coords(xml_root, sorted_data):
	'''Convert LRG co-ordinates to GRCh38 coordinates in BED format'''
	# Get GRCh38 data from xml_root (including coordinates)
	for item in xml_root.iter('mapping'):
		if item.attrib['coord_system'].startswith('GRCh38'):
			grch38 = item.attrib
			grch38_map = item.findall('mapping_span')[0].attrib
	# Empty list for new string
	output = []
	# Loop over LRG exon coordinates
	for xml_tuple in sorted_data:
		# Set LRG locations for reference genome
		genome_loc = int(grch38_map['other_start'])
		genome_loc2 = int(grch38_map['other_end'])
		exon_label, lrg_start_pre, lrg_end_pre = xml_tuple
		# Set LRG strat and end coordinates ( -1 for addition/subtraction from reference genome )
		lrg_start = int(lrg_start_pre) - 1
		lrg_end = int(lrg_end_pre) -1
		# If reverse strand, swap genome start and end, multiply lrg coordinates by -1 to subtract
		if grch38_map['strand'] == '-1':
			genome_loc = genome_loc2
			lrg_start, lrg_end = map(lambda x: x*-1, [lrg_start, lrg_end])
		# Set new coordinates tuple
		coords = (
			'chr' + str(grch38['other_name']),  # chromosome number
			str(genome_loc + lrg_start),  # grch38 start coordinates
			str(genome_loc + lrg_end)  # grch38 end coordinates
		)
		output.append(coords)
	return output

def main():
	'''Parse script input from command line arguments'''
	parser = argparse.ArgumentParser(description='Parse an XML file to produce a BED file')
	parser.add_argument('xml_file', nargs='+', help='Enter the names of the LRG file to parse')
	args = parser.parse_args()

	# store the output from lrg_parse() in a variable to write to a file
	files_to_parse = args.xml_file
	print('attempting to parse inputs: ' + ', '.join(files_to_parse))
	for f in files_to_parse:
		print('parsing ' + f)
		# call different functions depending on whether the XML file is 
		# on the system or needs to be accessed from the web
		if os.path.isfile(f):
			xml_string = parse_file(f)
			xml_root = set_root(xml_string)
			data = lrg_parse(xml_root)
		else:
			try:
				fname = f.upper()
				xml_string = get_file(fname)
				xml_root = set_root(xml_string)
				data = lrg_parse(xml_root)
			except ET.ParseError:
				print(f + ' does not exist.')
				continue
		# Convert exon regions to genomic coordinates for grch38
		output_bed = convert_coords(xml_root, data)
		write_file(output_bed, f)
		print('bed file for ' + f + ' complete.')
		
if __name__ == "__main__":
	main()