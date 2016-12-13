from PRNG import MT19937
from random import randint
import time

def random_data(length):
	return ''.join(chr(randint(0,255)) for i in range(length))

used_key = randint(0,2**16-1)

def XOR(A, B):
	if (len(B) > len(A)):
		return XOR(B,A)
	return ''.join(chr(ord(A[i])^ord(B[i%len(B)])) for i in range(len(A)))

def encrypt(data, key):
	m = MT19937(key & 0xFFFF )
	keystream = ''.join(chr(m.random() & 0xFF ) for i in range(len(data)))
	return XOR(data,keystream)

def decrypt(data, key):
	return encrypt(data, key)

def CTR_oracle(data):
	txt = random_data(randint(2,50)) + data
	return encrypt(txt, used_key)

def generate_pass_reset_token():
	seed = int(time.time()) & 0xFFFF
	txt = 'A'*randint(2,20)
	return encrypt(txt, seed)

def is_token_from_current_time(token):
	seed = int(time.time()) & 0xFFFF
	txt = 'A'*len(token)
	return encrypt(txt,seed) == token

def crack_CTR_oracle(oracle):
	txt = 'A'*14
	cipher = oracle(txt)
	keystream = XOR(cipher,txt)
	possible_seeds=[]

	for x in range(2**16):
		m = MT19937(x)
		guessed_keystream = ''.join(chr(m.random() & 0xFF ) for i in range(len(cipher)))

		for i in range(len(cipher)-14+1):
			if (keystream[i:i+14] in guessed_keystream ) :
				possible_seeds.append(x)
				
	print 'Used seed : '+str(used_key)
	print 'Guessed seeds : ', possible_seeds
	if (used_key in possible_seeds ):
		print '[+] Cracked : Used seed in Guessed seeds'


if __name__ == '__main__':
	txt = random_data(randint(2,50))
	key = randint(0,2**16-1)
	if (decrypt(encrypt(txt, key), key) == txt):
		print '[+] Test passed : decrypt(encrypt(txt, key), key) == txt ' 

	print '\nHacking begins ...\n'
	crack_CTR_oracle(CTR_oracle)

	if(is_token_from_current_time(generate_pass_reset_token())):
		print '[+] Token from current time verified'