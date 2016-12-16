from AES_128 import AES_128_ECB_decrypt,AES_128_CTR,random_data,XOR
from base64 import b64decode
from random import randint

random_key = random_data(16)

def edit(ciphertext, offset, newtext):
	pt = AES_128_CTR(txt, random_key)
	pt = pt[:offset] + newtext + pt[offset+len(newtext):]
	return AES_128_CTR(pt, random_key)

def crack(cipher, oracle):
	attack = 'A'*len(cipher)
	keystream = XOR (attack, oracle(cipher, 0, attack))
	pt = XOR(cipher, keystream)
	return pt

if __name__ == '__main__':
	
	cipher = ''.join(line.strip() for line in open('25.txt','r'))
	txt = AES_128_ECB_decrypt(b64decode(cipher), 'YELLOW SUBMARINE', True)

	cipher = AES_128_CTR(txt, random_key)

	newtext = random_data(randint(10,50))
	offset = randint(0,len(cipher)-1)
	
	if AES_128_CTR(edit(cipher, offset, newtext), random_key)[offset:offset+len(newtext)] == newtext :
		print '[+] Edit Test passed'
	else :
		print '[-] Failed'

	print '[+] Cracked \n'crack(cipher, edit)