#update 16x9.mpg and 4x3.mpg string with HD.mpg string in xml file
import xml.etree.ElementTree as ET
import sys

tag = "stream"
attr = "FileName"

def updateStr(s, upd):
	tmp = s.rsplit('_',1)[-1]
	return s.replace(tmp, upd)
	
def strReplace(s1, s2, s3):
	start = s1.find(s2)
	end = s1.find(".mpg")
	return s1[:start]+s3+s1[end:]
	
def readUpdate(fxml, ftxt):
	counter = 0
	txtfile = open(ftxt, "r")
	txttable = []
	for t in txtfile:
		txttable.append(t)
	txtfile.close()
	print "[+] reading xml!"
	xml = ET.parse(fxml)
	root = xml.getroot()
	for child in root.iter(tag):
		tmp = child.attrib[attr]
		for tline in txttable:
			rline = tmp.find(tline.rstrip())
			if rline != -1:
				counter += 1
				child.attrib[attr] = updateStr(tline, "HD.mpg")
	print "[+] Updated %s " % counter
	xml.write('result.xml')

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file.xml>; <file.txt>;"
else:
	readUpdate(sys.argv[1], sys.argv[2])