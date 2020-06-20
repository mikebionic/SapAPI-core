from random import randint

def makeRegNum(shortName,prefix,lastNum,suffix,random_mode=None):
	if random_mode:
		lastNum = randint(1,10000)
	regNo = shortName+prefix+str(lastNum)+suffix
	return regNo

regNo = makeRegNum('AS','SF',13,'',True)

print(regNo)