#compare two text files;
import sys

def updateStr(s, upd):
	return s[:-9]+upd
	
def strReplace(s1, s2, s3):
	start = s1.find(s2)
	end = s1.find(".mpg")
	return s1[:start]+s3+s1[end:]
#compare two text files;
def findReplaceWith(s1, s2, s3):
	return s1.replace(s2, s3, 1)
	
def checkLstForDublicatedLine(lst, line):
	if (line in lst):
		return True
	else:
		return False
	
def txtCompare(stxt, dtxt):
	sTmp = []
	tmpNotFoundedLst = []
	founded = 0
	notfounded = 0
	sourceFile = open(stxt, "r")
	destFile = open(dtxt, "r")
	sTable = []
	dTable = []
	for s in sourceFile:
		sTable.append(s.strip())
	sourceFile.close()
	for d in destFile:
		dTable.append(d.strip())
	destFile.close()
	for i in range(len(sTable)):
		sTmp = sTable[i]
		for j in range(len(dTable)):
			if dTable[j].find(sTable[i]) != -1:
				founded+=1
				sTmp = ''
				break
		if sTmp == sTable[i]:
			notfounded+=1
	print "[+] Founded=%s" % founded
	print "[+] Not Founded %s" % notfounded

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <compare.txt> <with.txt>"
else:
	txtCompare(sys.argv[1], sys.argv[2])