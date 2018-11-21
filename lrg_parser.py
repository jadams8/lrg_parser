import xml.etree.ElementTree as ET

lrg1 = ET.parse('data/LRG_1.xml')
root = lrg1.getroot()

print(root.tag, root.attrib)

for exon in root.iter('exon'):
	if 'label' in exon.attrib.keys():
		print(exon.tag, exon.attrib)