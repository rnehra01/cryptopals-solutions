from random import randint
from base64 import b64decode,b64encode
from AES_128 import AES_128_CBC_decrypt,AES_128_CBC_encrypt,pkcs_7_unpad,XOR,random_data

IV = random_data(16)

def check_high_ASCII(data):
	for c in data:
		if ord(c) > 127 :
			raise ValueError(data)

def encryption_oracle(data):
	return AES_128_CBC_encrypt(data,IV)

def decryption_oracle(data):
	txt = AES_128_CBC_decrypt(data,IV)
	check_high_ASCII(txt)
	return txt

def crack():
	cipher = encryption_oracle('A'*80)
	attack = cipher[0:16]+'\x00'*16+cipher[0:16]+cipher[-32:]
	recovered_pt = ''
	try:
		recovered_pt = decryption_oracle(attack)
	except ValueError as e:
		recovered_pt = str(e) 

	key = XOR(recovered_pt[0:16],recovered_pt[32:48])
	if key == IV :
		print '[+] Cracked key : %s' % repr(key)


if __name__ == '__main__':

	try:
		decryption_oracle(encryption_oracle('0123456798abcde\x96'))
	except ValueError as e:
		print '[+] High-ASCII Detection Test Passed'

	crack()

	
		
	