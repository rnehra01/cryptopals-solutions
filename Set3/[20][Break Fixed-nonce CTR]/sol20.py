from AES_128 import AES_128_CTR,random_data,XOR
from base64 import b64decode,b64encode

random_key=random_data(16)

def single_byte_xor_key(cipher):   #returns the key
	f=[]
		
	for i in xrange(0,256):
		f.append(0)
		decrypted=''

		for c in cipher:
			decrypted+=chr(i^ord(c))

		for c in decrypted:
			if ((ord(c)>=65 and ord(c)<=90) or (ord(c)>=97 and ord(c)<=122) or ord(c)==32) : #Calculating the no of alphabets in string decrypted with key i
				f[i]+=1

	max_f=0
	key=0
	for i in xrange(0,256):
		if (max_f<f[i]):
			max_f=f[i]
			key=i

	return chr(key)

def crack(ciphers):
	key=''
	max_len=max(len(c) for c in ciphers)

	for i in range(max_len):
		#Xor key for the i-th byte
		ith_cipher=''											
		for c in ciphers:
			try:
				ith_cipher+=c[i]
			except:
				pass
		key+=single_byte_xor_key(ith_cipher)

	print '[+] Cracked KEY : '+key
	print '[+] Decrypting Cipher'
	for c in ciphers:
		print XOR(c,key[:len(c)])

if __name__ == '__main__':
	
	ciphers=[]
	for line in open('20.txt'):
		ciphers.append(AES_128_CTR(b64decode(line.strip()),random_key))

	crack(ciphers)
