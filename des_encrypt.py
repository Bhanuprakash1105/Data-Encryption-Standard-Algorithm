import DESboxes

def giveBin(s):
	result = ""
	for c in s:
		binc = bin(int(c, 16)).zfill(4)
		binc = binc[binc.find('b') + 1::]
		if len(binc) > 4:
			assert False
		elif len(binc) < 4:
			binc = "0"*(4 - len(binc)) + binc
		result += binc
	return result

def permute(box, textBin):
	result = ""
	for i in range(len(box)):
		result += textBin[box[i] - 1]
	return result

def giveChar(b):
	result = ""
	for i in range(0, len(b), 4):
		chBin = b[i:i+4:1]
		ch = hex(int(chBin, 2))
		ch = ch[ch.find('x') + 1::]
		result += ch
	return result.upper()

def shiftLeft(s, i):
	noshifts = 2
	doubleshiftList = [1, 2, 9, 16]
	if i in doubleshiftList:
		noshifts -= 1
	r = s[noshifts::]+s[0:noshifts]
	return r

def key_gen(keytext):
	keytextBin = giveBin(keytext)
	prdroptext = permute(DESboxes.parityDropbox, keytextBin)
	a = prdroptext[0:28]
	b = prdroptext[28:]
	keys = []
	for i in range(1, 17, 1):
		a = shiftLeft(a, i)
		b = shiftLeft(b, i)
		cpoutbin = permute(DESboxes.compressionPbox, a + b)
		keys.append(giveChar(cpoutbin))
	return keys

def initial_permutation(plaintext):
	plaintextBin = giveBin(plaintext)
	outputtextBin = permute(DESboxes.initialPermuteBox, plaintextBin)
	outputtext = giveChar(outputtextBin)
	return outputtext

def substitute(sboxes, textBin):
	result = ""
	s = 0
	for i in range(0, len(textBin), 6):
		bit6 = textBin[i:i+6]
		rowbin = bit6[0] + bit6[5]
		columnbin = bit6[1:5]
		rowDec = int(rowbin, 2)
		columnDec = int(columnbin, 2)
		valueDec = sboxes[s][rowDec][columnDec]
		valBin = bin(valueDec).replace("0b", "")
		if len(valBin) > 4:
			assert False
		elif len(valBin) < 4:
			valBin = "0"*(4 - len(valBin)) + valBin
		result += valBin
		s += 1
	return result

def xorfunc(abin, bbin):
	assert len(a) == len(b)
	result = ""
	for i in range(len(abin)):
		if abin[i] == bbin[i]:
			result += '0'
		else:
			result += '1'
	return result

def DESfunc(text, key):
	textbin = giveBin(text)
	epboxout = permute(DESboxes.expansionPbox, textbin)
	xorout = xorfunc(epboxout, giveBin(key))
	subout = substitute(DESboxes.substitionBox, xorout)
	resBin = permute(DESboxes.straightPbox, subout)
	return giveChar(resBin)

plaintext = input("\nEnter input string: ")
keytext =   input("\nEnter the key text: ")
keys16 = key_gen(keytext)
plaintextPermuted = initial_permutation(plaintext)
print("\n>> Step1 output = {} = {}\n".format(plaintextPermuted, giveBin(plaintextPermuted)))
a = plaintextPermuted[0:8]
b = plaintextPermuted[8::]
for i in range(1, 17, 1):
	bfunc = DESfunc(b, keys16[i - 1])
	xor_res = xorfunc(giveBin(a), giveBin(bfunc))
	xor_res = giveChar(xor_res)
	if i == 16:
		a = xor_res
	else:
		temp = b
		b = xor_res
		a = temp
	print("> Round{:3d} => Left = {}  Right = {}  Round_key = {}".format(i, a, b, keys16[i-1]))
print("\n>> Step2 output = {} = {}".format(a + b, giveBin(a + b)))
ciphertext = permute(DESboxes.finalPermuteBox, giveBin(a + b))
ciphertext = giveChar(ciphertext)
print("\n>> Step3 Cipher = {} = {}".format(ciphertext, giveBin(ciphertext)))
print("")