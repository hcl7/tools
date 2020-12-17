import sys

def updateStr(s, upd):
	return s[:-9]+upd
	
def strReplace(s1, s2, s3):
	start = s1.find(s2)
	end = s1.find(".mpg")
	return s1[:start]+s3+s1[end:]

def findReplaceWith(s1, s2, s3):
	return s1.replace(s2, s3, 1)
	
def readUpdate(stxt, dtxt):
	founded = 0
	notfound = 0
	sourceFile = open(stxt, "r")
	destFile = open(dtxt, "r")
	sTable = []
	dTable = []
	for s in sourceFile:
		sTable.append(s)
	sourceFile.close()
	for d in destFile:
		dTable.append(d)
	destFile.close()
	notFoundedFile = open("notFounded.txt", "w+")
	foundedFile = open("Founded.txt", "w+")
	for i in range(len(sTable)):
		sTmp = sTable[i]
		for j in range(len(dTable)):
			if dTable[j].find(sTable[i]) != -1:
				founded += 1
				foundedFile.write(sTable[i])
				sTmp = ""
				break
		if sTmp == sTable[i]:
			notfound += 1
			notFoundedFile.write(sTable[i])
	print "[+] Founded=%s" % founded
	print "[+] Not Founded %s" % notfound
	notFoundedFile.close()
	foundedFile.close()

if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <compare.txt> <with.txt>"
else:
	readUpdate(sys.argv[1], sys.argv[2])
	
