#remove duplicated lines of a text file;
import sys

def checkLstForDublicatedLine(lst, line):
	if (line in lst):
		return True
	else:
		return False

def rmDeplicatedLines(txt):
	tmpNotFoundedLst = []
	counter = 0
	txtfile = open(txt, "r")
	txttable = []
	for t in txtfile:
		txttable.append(t)
	txtfile.close()
	resultfile = open("withoutDeplicates.txt", "w+")
	for tline in txttable:
		if (checkLstForDublicatedLine(tmpNotFoundedLst, tline) == False):
			counter+=1
			resultfile.write(tline)
		tmpNotFoundedLst.append(tline)
	print "[+] Duplicated Removed=%s" % (len(txttable) - counter)
	resultfile.close()
	
if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file.txt>"
else:
	rmDeplicatedLines(sys.argv[1])