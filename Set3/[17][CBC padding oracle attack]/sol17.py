from oracles import encryption_oracle,padding_oracle,random_IV
from AES_128 import XOR,pkcs_7_unpad

def find_nxt_chr(cipher,pr_block,cur_block,known,oracle):
	k   =15-len(known)										   #kth chr to be decrypted in the block
	C0  =pr_block											   
	P   ='X'*(16-len(known)-1)+'?'+known
	_P  ='X'*(16-len(known)-1)+chr(len(known)+1)*(len(known)+1)
	_C0 =XOR(XOR(_P,P),C0)

	for c in range(256):
		_C0=_C0[0:k]+chr(c)+_C0[k+1:]
		attack=_C0+cur_block
		if (oracle(attack)):
			return XOR(XOR(_P[k],chr(c)),C0[k])

def crack(data,oracle):
	no_of_blocks=len(data)/16
	blocks=[random_IV]
	for block_no in range(no_of_blocks):
		blocks.append(data[block_no*16:(block_no+1)*16])
	
	msg=''
	for i in range(1,len(blocks)):
		block_msg=''
		for j in range(16):
			try:
				block_msg=find_nxt_chr(data,blocks[i-1],blocks[i],block_msg,oracle)+block_msg
			except:
				pass
		msg+=block_msg

	return (msg)

if __name__ == '__main__':
	msg=[]
	
	while True:
		try:
			if (len(msg)==10):
				break
			cracked_msg=pkcs_7_unpad(crack(encryption_oracle(),padding_oracle))
			if ( not (cracked_msg in msg)):
				msg.append(cracked_msg)
				print cracked_msg
		except:
			print 'EX'