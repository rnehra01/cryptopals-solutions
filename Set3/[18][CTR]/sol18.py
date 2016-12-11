from AES_128 import AES_128_ECB_encrypt,XOR
from base64 import b64decode

KEY='YELLOW SUBMARINE'

def int_TO_little_endian(x):
	x=hex(x)[2:]
	if (len(x)!=32):
		x='0'*(32-len(x))+x
	x=x.decode('hex')

	converted=''
	for i in reversed(x[:8]):
		converted+=i
	for i in reversed(x[8:]):
		converted+=i
	return converted

def AES_128_CTR(data,key,nonce=0):
	from math import ceil
	keystream=''
	for i in range(int(ceil(len(data)/16.0))):
		keystream+=AES_128_ECB_encrypt(int_TO_little_endian(nonce),key,False)
		nonce+=1
	keystream=keystream[:len(data)]

	return XOR(data,keystream)

if __name__ == '__main__':
	data='L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
	print '[+] Decrypted : "'+AES_128_CTR(b64decode(data),KEY)+'"'	
