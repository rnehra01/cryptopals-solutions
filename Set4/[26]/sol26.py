from random import randint
from base64 import b64decode,b64encode
from AES_128 import AES_128_CTR,pkcs_7_unpad,XOR,random_data

random_key = random_data(16)

def encryption_oracle(data):
	str1='comment1=cooking%20MCs;userdata='
	str2=';comment2=%20like%20a%20pound%20of%20bacon'
	data=data.replace(';','')
	data=data.replace('=','')
	txt=str1+data+str2

	return AES_128_CTR(txt,random_key)

def verify_admin(data):
	txt=AES_128_CTR(data,random_key)
	return True if (';admin=true;' in txt) else False

def len_of_prefix(oracle):
	cp1 = oracle('a'*5)
	cp2 = oracle('b'*10)
	for i in range(len(cp1)):
		if (cp1[i] != cp2[i]):
			return i-1

def create_admin(oracle):
	prefix_len = len_of_prefix(oracle)
	inp = 'A'*16
	cipher = oracle(inp)
	keystream = XOR (inp, cipher[prefix_len:prefix_len+16])
	attack = cipher[:prefix_len] + XOR('XXXX;admin=true;', keystream) + cipher[prefix_len+16:]
	return attack if verify_admin(attack) else False

if __name__ == '__main__':

	print '[+] Access Granted' if create_admin(encryption_oracle) else '[-] Access Denied'
		
	