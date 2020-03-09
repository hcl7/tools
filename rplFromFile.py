#replace first string until ; char with second string after ; char 
#and update xml file
#first file: str1;str2
#second file: str1

import xml.etree.ElementTree as ET
import sys

__author__ = 'Elvin SEVEN Mucaj'
tag = "stream"
attr = "FileName"

def fileToList(self, fn):
	txtfile = open(fn, "r")
	txtlst = []
	for t in txtfile:
		txtlst.append(t.rstrip())
	txtfile.close()
	return txtlst
	
def lineToFile(self, line, f):
	resultfile = open(f, "w")
	resultfile.write(line)
	resultfile.close()
	
def findReplaceWith(s1, s2, s3):
	return s1.replace(s2, s3, 1)
	
def strReplace(s1, s2, s3):
	start = s1.find(s2)
	end = s1.find(".mpg")
	return s1[:start]+s3+s1[end:]
	
def getStringUntilChar(str, char):
	return str[:str.find(char) + len(char)-1]

def getStringAfterChar(str, char):
	return str[str.find(char) + len(char):]

def readUpdate(fxml, ftxt):
	counter = 0
	txtfile = open(ftxt, "r")
	txttable = fileToList(txtfile)
	print "[+] reading xml!"
	xml = ET.parse(fxml)
	root = xml.getroot()
	for child in root.iter(tag):
		tmp = child.attrib[attr]
		for tline in txttable:
			before = getStringUntilChar(tline, ";").rstrip()
			after = getStringAfterChar(tline, ";").rstrip()
			rline = tmp.find(before)
			if rline != -1:
				counter += 1
				child.attrib[attr] = findReplaceWith(tmp, before, after)
	print "[+] Updated %s " % counter
	xml.write('result.xml')

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file.xml> <file.txt>"
else:
	readUpdate(sys.argv[1], sys.argv[2])