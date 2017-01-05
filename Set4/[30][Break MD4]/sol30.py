from struct import pack, unpack
from MD4 import MD4

def cal_MD4_pad(msg):
	n = len(msg) 
	bit_len = n * 8
	index = (bit_len >> 3) & 0x3fL
	pad_len = 120 - index
	if index < 56:
		pad_len = 56 - index
	padding = '\x80' + '\x00'*63
	padding = padding[:pad_len] + pack('<Q', bit_len)
	return padding

def oracle(data):
	key = 's3cr3tk5y'
	m = MD4()
	m.update(key + data)
	return m.digest()

def check_admin(data, hash_tag):
	if ( not 'admin=true' in data):
		return False
	# Check authencity of data
	if (oracle(data) == hash_tag):
		return True

if __name__ == '__main__':

	msg = 'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
	msg_MD4 =oracle(msg)

	print 'Let the HACK begin ...\n'

	for key_length in range(15):
		print 'Trying key length : %d' % key_length

		attack_msg = msg + cal_MD4_pad(key_length*'a' + msg) + ';admin=true'
		
		# msg_MD4 is used to get internal state
		last_internal_state = unpack('<IIII', msg_MD4.decode('hex'))
		m = MD4(last_internal_state[0], last_internal_state[1], last_internal_state[2], last_internal_state[3])
		m.update(';admin=true', 
			key_length +len( msg + cal_MD4_pad(key_length*'a' + msg)))
		attack_hash = m.digest()
		
		if (check_admin(attack_msg, attack_hash)):
			print '[+] Hacked'
			print 'Tampered message : %s' % attack_msg
			print 'Hash : %s' % attack_hash
			break
		else :
			print '[-] Nope'