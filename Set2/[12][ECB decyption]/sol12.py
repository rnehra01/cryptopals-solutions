from random import randint
from base64 import b64decode,b64encode
from AES_128 import AES_128_ECB_encrypt,pkcs_7_unpad

unknown_str=b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

def random_data(len):
	data=''
	for x in xrange(0,len):
		data+=chr(randint(0,255))
	return data

random_key=random_data(16)

def encryption_oracle(txt,key=random_key):

	txt=txt+unknown_str
	return AES_128_ECB_encrypt(txt,key,True)

def len_of_cipher_block(oracle):
	inp='A'
	initial_len=len(oracle(inp,random_key))

	while True:
		inp+='A'
		l=len(oracle(inp,random_key))
		if (l>initial_len):
			return (l-initial_len)

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
	msg=''
	for i in range(0,len(oracle(''))):
		try:
			msg+=find_nxt_chr(oracle,block_length,msg)
		except:
			break
	return pkcs_7_unpad(msg)


if __name__ == '__main__':
	print '\nDecrypted Text \n\n'+crack(encryption_oracle)	
	


