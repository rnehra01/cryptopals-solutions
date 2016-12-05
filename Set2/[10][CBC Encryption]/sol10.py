from Crypto.Cipher import AES
from base64 import b64decode,b64encode


def pkcs_7_pad(txt):
	block_length=16

	pad_len=0
	if (len(txt)%block_length==0):
		pad_len=block_length
	else :
		pad_len=block_length-len(txt)%block_length

	return txt+chr(pad_len)*pad_len

def pkcs_7_unpad(txt):
	block_length=16
	
	pad_len=ord(txt[-1])
	return txt[:-pad_len]

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

def AES_128_CBC_decrypt(txt,key,IV):
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

def main():
	cipher=''
	f=open('10.txt','r')
	for l in f:
		cipher+=l.strip()

	key='YELLOW SUBMARINE'
	IV='\x00'*16
	
	pt=AES_128_CBC_decrypt(b64decode(cipher),key,"\x00"*16)
	print pt

	encrypted=b64encode(AES_128_CBC_encrypt(pt,key,IV))
	print encrypted
	if (encrypted==cipher):
		print "Good JOB!!!"

if __name__ == '__main__':
	main()