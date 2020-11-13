#Find pattern before ; char from first file one
#Get pattern after ; char from file one
#Match pattern before ; char from file one with line of file two
#Write after ; char to result file
import sys

__author__ = 'Elvin SEVEN Mucaj'

def fileToList(fn):
	txtfile = open(fn, "r")
	txtlst = []
	for t in txtfile:
		txtlst.append(t.rstrip())
	txtfile.close()
	return txtlst
	
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

def findPatternInString(fxml, ftxt):
	counter = 0
	xmltable = []
	txttable = []
	xmltable = fileToList(fxml)
	txttable = fileToList(ftxt)
	resultfile = open("Founded.txt", "w+")
	for rline in xmltable:
		for tline in txttable:
			before = getStringUntilChar(rline, ";").rstrip()
			after = getStringAfterChar(rline, ";").rstrip()
			tmp = tline.find(before)
			if tmp != -1:
				counter += 1
				resultfile.write(after+'\n')
	print "[+] Founded %s " % counter
	resultfile.close()

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file1.txt> <file2.txt>"
else:
	findPatternInString(sys.argv[1], sys.argv[2])
