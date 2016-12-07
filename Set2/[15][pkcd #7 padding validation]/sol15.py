

def validate_pkcs_7_pad(data,block_length=16):

	if (len(data)%block_length):
		return False

	pad_byte=pad_len=data[-1]
	pad_len=ord(data[-1])
	if (data[-pad_len:]!=pad_byte*pad_len):
		return False

	return True

def pkcs_7_pad(txt,block_length=16):

	pad_len=0
	if (len(txt)%block_length==0):
		pad_len=block_length
	else :
		pad_len=block_length-len(txt)%block_length

	return txt+chr(pad_len)*pad_len

class paddingError(Exception):
	'''Exception for incorrect padding'''

def pkcs_7_unpad(data,block_length=16):
	if (validate_pkcs_7_pad(data,block_length)):
		pad_len=ord(data[-1])
		return data[:-pad_len]
	else:
		raise paddingError

if __name__ == '__main__':
	testCases=["ICE ICE BABY\x04\x04\x04\x04","ICE ICE BABY\x05\x05\x05\x05","ICE ICE BABY\x01\x02\x03\x04"]
	for s in testCases:
		try:
			print pkcs_7_unpad(s)
		except paddingError:
			print 'Improper padding, paddingError exception CAUGHT'