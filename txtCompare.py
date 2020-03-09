#compare two text files;
import sys

def updateStr(s, upd):
	return s[:-9]+upd
	
def strReplace(s1, s2, s3):
	start = s1.find(s2)
	end = s1.find(".mpg")
	return s1[:start]+s3+s1[end:]

def findReplaceWith(s1, s2, s3):
	return s1.replace(s2, s3, 1)
	
def checkLstForDublicatedLine(lst, line):
	if (line in lst):
		return True
	else:
		return False
	
def txtCompare(stxt, dtxt):
	tmpNotFoundedLst = []
	founded = 0
	notfounded = 0
	sourceFile = open(stxt, "r")
	destFile = open(dtxt, "r")
	sTable = []
	dTable = []
	for x in sourceFile:
		sTable.append(x)
	sourceFile.close()
	for t in destFile:
		dTable.append(t)
	destFile.close()
	resultfile = open("notFounded.txt", "w+")
	resultfile2 = open("Founded.txt", "w+")
	for xline in sTable:
		tmpXline = xline
		for tline in dTable:
			rline = xline.find(tline)
			if rline != -1:
				founded += 1
				resultfile2.write(xline)
				xline = ""
		if tmpXline == xline:
			if (checkLstForDublicatedLine(tmpNotFoundedLst, xline) == False):
				notfounded += 1
				resultfile.write(xline)
			tmpNotFoundedLst.append(xline)
	print "[+] Founded=%s" % founded
	print "[+] Not Founded %s" % notfounded
	resultfile.close()
	resultfile2.close()

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <compare.txt> <with.txt>"
else:
	txtCompare(sys.argv[1], sys.argv[2])