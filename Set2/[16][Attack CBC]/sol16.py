from random import randint
from base64 import b64decode,b64encode
from AES_128 import AES_128_CBC_encrypt,AES_128_CBC_decrypt,pkcs_7_unpad,XOR

def random_data(len):
	data=''
	for x in xrange(0,len):
		data+=chr(randint(0,255))
	return data

random_key=random_data(16)

def encryption_oracle(data):
	str1='comment1=cooking%20MCs;userdata='
	str2=';comment2=%20like%20a%20pound%20of%20bacon'
	data=data.replace(';','')
	data=data.replace('=','')
	txt=str1+data+str2

	return AES_128_CBC_encrypt(txt,random_key)

def verify_admin(data):
	txt=AES_128_CBC_decrypt(data,random_key)
	if (';admin=true;' in txt):
		return True
	else :
		return False

def create_admin(oracle):
	inp='A'*16+'XadminXtrueXAAAA'
	cp=oracle(inp)
	req_decrypted_block=';admin=true;AAAA'
	#Now modify the cp block corresponding to 'A'*16 so that next block on decrypion gives req_decrypted_block
	attack=XOR(XOR('XadminXtrueXAAAA',req_decrypted_block),cp[32:48])+cp[48:]	
	
	if (verify_admin(attack)):
		return attack

if __name__ == '__main__':
	attack_txt=create_admin(encryption_oracle)

	print 'You are r00t' if verify_admin(attack_txt) else 'Script Kiddies NOT allowed'
		
	