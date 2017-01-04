# Lenght-extension attack
# https://blog.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks
from SHA1 import __SHA1

# Generates hex-encoded padding 
def calculate_SHA_padding(data):
	ml = len(data)
	pad_len = 64 - (ml + 8)%64

	padding = '80' + (pad_len-1)*'00' + hex(ml*8)[2:].rjust(16, '0')  
	return padding

def oracle(data):
	key = 's3cr3tk5y'
	return __SHA1(key + data).hash()

def check_admin(data, hash_tag):
	if ( not 'admin=true' in data):
		return False
	# Check authencity of data
	if (oracle(data) == hash_tag):
		return True


if __name__ == '__main__':

	msg = 'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
	msg_sha1 =oracle(msg)

	print 'Let the HACK begin ...\n'

	for key_length in range(15):
		print 'Trying key length : %d' % key_length

		attack_msg = msg + calculate_SHA_padding(key_length*'a' + msg).decode('hex') + ';admin=true'
		
		# msg_sha1 is used to get internal state
		attack_hash = __SHA1(';admin=true', 
			key_length +len( msg + calculate_SHA_padding(key_length*'a' + msg).decode('hex')),
			int(msg_sha1[:8],16), int(msg_sha1[8:16],16), int(msg_sha1[16:24],16), int(msg_sha1[24:32],16), int(msg_sha1[32:],16)).hash()
		
		if (check_admin(attack_msg, attack_hash)):
			print '[+] Hacked'
			print 'Tampered message : %s' % attack_msg
			print 'Hash : %s' % attack_hash
			break
		else :
			print '[-] Nope'