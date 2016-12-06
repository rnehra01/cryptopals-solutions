from random import randint
from AES_128 import AES_128_ECB_encrypt,AES_128_ECB_decrypt,pkcs_7_pad,pkcs_7_unpad

def random_data(len):
	data=''
	for x in xrange(0,len):
		data+=chr(randint(0,255))
	return data

random_key=random_data(16)

def profile_for(email):
	email=email.replace('&','')
	email=email.replace('=','')
	return 'email='+email+'&uid=10'+'&role=user'

def parse_str(data):
	parsed_arr={}
	for c in data.split('&'):
		try:
			parsed_arr[c.split('=')[0]]=c.split('=')[1]
		except:
			pass
	return parsed_arr

def encrypted_profile_for(email,key=random_key):
	return AES_128_ECB_encrypt(profile_for(email),key,True)

def decrypt_profile(profile,key=random_key):
	return AES_128_ECB_decrypt(profile,key,True)

def verify_admin(profile):
	decrypted_profile=decrypt_profile(profile)
	if (parse_str(decrypted_profile)['role']=='admin'):
		return True
	else:
		return False

def malicious_profile(oracle):

	# 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 0123456789ABCDEF 
	# email=aaaaaaaaaa aaa&uid=10&role= user------------
	encrypted_id_role=oracle('a'*13)[16:32]
	encrypted_email  =oracle('a'*13)[0:16]
	# email=aaaaaaaaaa admin----------- &uid=10&role=use r
	encrypted_admin  =oracle('a'*10+pkcs_7_pad('admin'))[16:32]
	# email=aaaaaaaaaa aaa&uid=10&role= admin-----------
	encrypted_profile=encrypted_email+encrypted_id_role+encrypted_admin
	return encrypted_profile

def crack(oracle):
	encrypted_malicious_profile=malicious_profile(oracle)
	if (verify_admin(encrypted_malicious_profile)):
		print 'You are authorised.'

if __name__ == '__main__':
	crack(encrypted_profile_for)

	