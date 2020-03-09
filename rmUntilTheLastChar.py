#file: \\server\path\file.mpg
#result: file.mpg
import sys

def removeUntilTheLastCharacter(s, c):
	return s.rsplit(c,1)[-1]

def fileToList(fn):
	txtfile = open(fn, "r")
	txtlst = []
	for t in txtfile:
		txtlst.append(t.rstrip())
	txtfile.close()
	return txtlst
	
def run(f, c):
	tmp = fileToList(f)
	resultfile = open("filesAll.txt", "w+")
	for line in tmp:
		resultfile.write(removeUntilTheLastCharacter(line,c)+'\n')
	resultfile.close()
	print "[+] Done!!!"
	
if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file1.txt> <character>"
else:
	run(sys.argv[1], sys.argv[2])