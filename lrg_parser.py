import xml.etree.ElementTree as ET
import os, argparse, fnmatch, re, requests


def parse_file(xml_file):
	lrg = ET.parse(xml_file)
	root = lrg.getroot()
	return root

def lrg_parse(root):
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
	return convert_coords(root, sorted_data)

def write_file(data, file_name):
	with open(file_name, 'w') as myfile:
		for my_tuple in data:
			# reformat the list to tab seperated and different lines
			my_list = "\t".join(my_tuple) + '\n'
			myfile.write(my_list)

def get_file(lrg_num):
	website = 'http://ftp.ebi.ac.uk/pub/databases/lrgex/'+ lrg_num +'.xml'
	xml_text = requests.get(website)
	if xml_text.status_code == 404:
		website = 'http://ftp.ebi.ac.uk/pub/databases/lrgex/pending/'+ lrg_num +'.xml'
		xml_text = requests.get(website)
	root = ET.fromstring(xml_text.text)
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
		genome_loc1 = int(grch38_map['other_start'])
		genome_loc2 = int(grch38_map['other_end'])
		exon_label, lrg_start_pre, lrg_end_pre = xml_tuple
		print(xml_tuple)
		# Set LRG strat and end coordinates ( -1 for addition/subtraction from reference genome )
		lrg_start = int(lrg_start_pre) - 1
		lrg_end = int(lrg_end_pre) -1
		# If reverse strand, swap genome start and end, multiply lrg coordinates by -1 to subtract
		print(grch38_map['strand'])
		if grch38_map['strand'] == '-1':
			genome_loc1, genome_loc2 = genome_loc2, genome_loc1
			lrg_start, lrg_end = map(lambda x: x*-1, [lrg_start, lrg_end])
		# Set new coordinates tuple
		coords = (
			'chr' + str(grch38['other_name']),  # chromosome number
			str(genome_loc1 + lrg_start),  # grch38 start coordinates
			str(genome_loc1 + lrg_end)  # grch38 end coordinates
		)
		print(coords)
		output.append(coords)
	return output


def main():
	parser = argparse.ArgumentParser(description='Parse an XML file to produce a BED file')
	parser.add_argument('xml_file', nargs='+', help='Enter the names of the LRG file to parse')
	args = parser.parse_args()

	# store the output from lrg_parse() in a variable to write to a file
	files_to_parse = args.xml_file
	for f in files_to_parse:
		if os.path.isfile(f):
			data = lrg_parse(parse_file(f))
		else:
			data = lrg_parse(get_file(f))
		file_name = f.split('.')[0]+'.bed'
		write_file(data, file_name)
		
if __name__ == "__main__":
	main()