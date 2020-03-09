#check for dublicated lines in a text file;
import sys

def countWord(word, sentence):
	count = 0
	for i in range(len(sentence)):
		if sentence[i] == word:
			count += 1
	return count

def countedWords(word, sentence, n):
	found = False
	for i in range(n):
		if sentence[i] == word:
			found = True
	return found
  
def fileToList(fn):
	txtfile = open(fn, "r")
	txttable = []
	for t in txtfile:
		txttable.append(t.rstrip())
	txtfile.close()
	return txttable
  
def wordFrequency(sentence):
	for i in range(len(sentence)):
		if (countedWords(sentence[i], sentence, i) == True):
			continue
		else:
			c = countWord(sentence[i], sentence)
			if c > 1:
				print sentence[i] + '=%s' % countWord(sentence[i], sentence)
			
if len(sys.argv) < 2:
	print "[+] Usage: python",sys.argv[0]," <file.txt>;"
else:
	wordFrequency(fileToList(sys.argv[1]))
