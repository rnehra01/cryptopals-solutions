from random import randint
from base64 import b64decode,b64encode
from AES_128 import AES_128_ECB_encrypt,pkcs_7_unpad
from fractions import gcd

target_bytes=b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

def random_data(len):
	data=''
	for x in xrange(0,len):
		data+=chr(randint(0,255))
	return data

random_key=random_data(16)

def encryption_oracle(attacker_controlled,key=random_key):
	random_bytes=random_data(randint(0,200))
	txt=random_bytes+attacker_controlled+target_bytes
	return AES_128_ECB_encrypt(txt,key,True)

def len_of_cipher_block(oracle):
	#Exploiting the fact that cipher-length is a multiple of block-length
	l=len(oracle(random_data(randint(0,300))))
	for x in range(100):
		random_bytes=random_data(randint(0,300))
		l=gcd(l,len(oracle(random_bytes)))
	return l

def verify_ECB_mode(cipher,block_length):

	block_length=len_of_cipher_block(encryption_oracle)
	#To make at least two encrypted match, at least 3 blocks of matching text should be there
	pt=random_data(20)+'A'*randint(1,10)*block_length+random_data(30)+'A'*randint(2,10)*block_length
	cipher=encryption_oracle(pt)

	#Check whether cipher in ECB
	return is_ECB_encoded(cipher,block_length)

def is_ECB_encoded(cipher,block_length):

	for i in range(0,len(cipher)):
		for j in range(i+1,len(cipher)):
			if (cipher[i:i+block_length]==cipher[j:j+block_length]):
				return True
	return False

def rm_random_chrs(oracle,block_length):
	def simpler_oracle(data):
		while True:
			txt='a'*3*block_length+data
			cipher=oracle(txt)
			for i in range(len(cipher)):
				if ((cipher[i:i+16]==cipher[i+16:i+32]) and (cipher[i+16:i+32]==cipher[i+32:i+48])):
					return cipher[i+48:]

	return simpler_oracle

def find_nxt_chr(oracle,block_length,known_msg):
	
	req_block_len=(block_length-1-len(known_msg))%block_length
	req_block='A'*req_block_len

	for i in range(0,256):
		guessed_txt=req_block+known_msg+chr(i)
		l=len(guessed_txt)
	
		if (oracle(req_block)[:l]==oracle(guessed_txt)[:l]):
			return chr(i)


def crack(oracle):
	block_length=len_of_cipher_block(oracle)
	print 'Block-length : '+str(block_length)

	if (verify_ECB_mode(oracle,block_length)):
		print 'ECB mode verified'


	#real decryption starts
	oracle=rm_random_chrs(oracle,block_length)
	msg=''
	for i in range(0,len(oracle(''))):
		try:
			msg+=find_nxt_chr(oracle,block_length,msg)
			print msg
		except:
			pass
		
	return pkcs_7_unpad(msg)


if __name__ == '__main__':
	print '\nDecrypted Text \n'+crack(encryption_oracle)	
	
	
	


