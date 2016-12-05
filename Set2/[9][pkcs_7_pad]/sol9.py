
block_length=16

def pkcs_7_pad(txt):
	pad_len=0
	if (len(txt)%block_length==0):
		pad_len=block_length
	else :
		pad_len=block_length-len(txt)%block_length

	return txt+chr(pad_len)*pad_len

def pkcs_7_unpad(txt):
	pad_len=ord(txt[-1])
	return txt[:-pad_len]

if __name__ == '__main__':
	test='Crypto'
	if (pkcs_7_unpad(pkcs_7_pad(test))==test):
		print 'Paddind is my cup of tea.'
