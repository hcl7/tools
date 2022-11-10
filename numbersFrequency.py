def countNum(num, sentence):
	count = 0
	for i in range(len(sentence)):
		if sentence[i] == num:
			count += 1
	return count

def countedNums(num, sentence, n):
	found = False
	for i in range(n):
		if sentence[i] == num:
			found = True
	return found

def getMaxKeys(f):
    max_keys = [key for key, value in f.items() if value == max(f.values())]
    print(max_keys)

def numberFrepuency(sentence):
    f = {}
    for i in range(len(sentence)):
        if (countedNums(sentence[i], sentence, i) == True):
            continue
        else:
            c = countNum(sentence[i], sentence)
            if(c >= 1):
                print(sentence[i],'=', countNum(sentence[i], sentence))
                f[sentence[i]] = countNum(sentence[i], sentence)
    getMaxKeys(f)


l = [2,4,4,5,2,3,3,4,5,5,7,7,7,1]
numberFrepuency(l)
