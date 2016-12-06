from random import randint
from AES_128 import AES_128_ECB_encrypt,AES_128_CBC_encrypt

encryption_mode='NONE'

def random_data(len):
	data=''
	for x in xrange(0,len):
		data+=chr(randint(0,255))
	return data

def encryption_oracle(txt):
	global encryption_mode
	
	key=random_data(16)
	txt=random_data(randint(5,10))+txt+random_data(randint(5,10))
	IV =random_data(16)

	cipher=''
	if (randint(0,1)):
		cipher=AES_128_CBC_encrypt(txt,key,IV)
		encryption_mode='CBC'
	else:
		cipher=AES_128_ECB_encrypt(txt,key,True)
		encryption_mode='ECB'
	
	return cipher

def is_ECB_encoded(cipher,block_length=16):

	for i in range(0,len(cipher)):
		for j in range(i+1,len(cipher)):
			if (cipher[i:i+block_length]==cipher[j:j+block_length]):
				return True
	return False

def identify_encryption():
	block_length=16
	#To make at least two encrpted match, at least 3 blocks of matching text should be there
	pt=random_data(20)+'A'*randint(1,10)*block_length+random_data(30)+'A'*randint(2,10)*block_length
	cipher=encryption_oracle(pt)
	if (is_ECB_encoded(cipher)):
		return 'ECB'
	else:
		return 'CBC'

if __name__ == '__main__':
	for i in range(10):
		guess_encryption=identify_encryption()

		if guess_encryption==encryption_mode:
			print 'Identified '+ encryption_mode
		else:
			print 'Failed on '+ str(i)