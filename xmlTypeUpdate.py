#read xml file and update attribute value;
import xml.etree.ElementTree as ET
import sys

__author__ = 'Elvin SEVEN Mucaj'

tag = "DataBoxRecord"
attr = "type"

def typeUpdate(fxml, pattern):
	counter = 0
	print "[+] reading xml!"
	xml = ET.parse(fxml)
	root = xml.getroot()
	for child in root.iter(tag):
		counter += 1
		child.attrib[attr] = pattern
	print "[+] Updated %s " % counter
	xml.write('result.xml')

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file.xml> <type|ex: EXP3>"
else:
	typeUpdate(sys.argv[1], sys.argv[2])
