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
	return sorted_data

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
		print(website)
		xml_text = requests.get(website)
	root = ET.fromstring(xml_text.text)
	return root


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