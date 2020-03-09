#replace the values of attributes in the tag of xml file;
import xml.etree.ElementTree as ET
import sys

__author__ = 'Elvin SEVEN Mucaj'

tag = "DataBoxRecord"
attr1 = "clipid"
attr2 = "title"

def changeAttribValue(fxml):
	counter = 0
	print "[+] reading xml!"
	xml = ET.parse(fxml)
	root = xml.getroot()
	for child in root.iter(tag):
		counter += 1
		tmp = child.attrib[attr1]
		child.attrib[attr1] = child.attrib[attr2]
		child.attrib[attr2] = tmp
	print "[+] Updated %s " % counter
	xml.write('replaced.xml')

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file.xml>"
else:
	changeAttribValue(sys.argv[1])
