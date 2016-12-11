from Crypto.Cipher import AES
from base64 import b64decode,b64encode

from random import randint
def random_data(len):
	data=''
	for x in xrange(0,len):
		data+=chr(randint(0,255))
	return data

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

def validate_pkcs_7_pad(data,block_length=16):

	if (len(data)%block_length):
		return False

	pad_byte=pad_len=data[-1]
	pad_len=ord(data[-1])
	if (data[-pad_len:]!=pad_byte*pad_len):
		return False

	return True

def pkcs_7_pad(txt,block_length=16):

	pad_len=0
	if (len(txt)%block_length==0):
		pad_len=block_length
	else :
		pad_len=block_length-len(txt)%block_length

	return txt+chr(pad_len)*pad_len

class paddingError(Exception):
	'''Exception for incorrect padding'''

def pkcs_7_unpad(data,block_length=16):
	if (validate_pkcs_7_pad(data,block_length)):
		pad_len=ord(data[-1])
		return data[:-pad_len]
	else:
		raise paddingError

def XOR(txt,key):
	j=0
	ans=''
	for c in txt:
		ans+=chr(ord(c)^ord(key[j%len(key)]))
		j=j+1
	return ans

def AES_128_ECB_decrypt(txt, key, unpad=False):
	cipher=AES.new(key,AES.MODE_ECB)
	decrypted=cipher.decrypt(txt)
	if unpad:
		return pkcs_7_unpad(decrypted)
	return decrypted

def AES_128_ECB_encrypt(txt, key, pad=False):
	cipher=AES.new(key,AES.MODE_ECB)
	if pad:
		txt=pkcs_7_pad(txt)
	return cipher.encrypt(txt)

def AES_128_CBC_decrypt(txt,key,IV='\x00'*16):
	pt=''
	for x in range(len(txt),16,-16):
		pt=XOR(AES_128_ECB_decrypt(txt[x-16:x],key),txt[x-32:x-16])+pt
	pt=XOR(AES_128_ECB_decrypt(txt[0:16],key),IV)+pt
	return pkcs_7_unpad(pt)

def AES_128_CBC_encrypt(txt,key,IV='\x00'*16):
	cipher=''
	txt=pkcs_7_pad(txt)
	cipher+=AES_128_ECB_encrypt(XOR(txt[0:16],IV),key)
	for x in range(16,len(txt),16):
		cipher+=AES_128_ECB_encrypt(XOR(txt[x:x+16],cipher[x-16:x]),key)
	return cipher

def AES_128_CTR(data,key,nonce=0):
	from math import ceil
	keystream=''
	for i in range(int(ceil(len(data)/16.0))):
		keystream+=AES_128_ECB_encrypt(int_TO_little_endian(nonce),key,False)
		nonce+=1
	keystream=keystream[:len(data)]

	return XOR(data,keystream)
