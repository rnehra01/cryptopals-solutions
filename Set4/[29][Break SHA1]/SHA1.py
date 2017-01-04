
class __SHA1():
	"""SHA1 implementation"""
	'''
	data : new data if prev_data_len=0 else addidtional forge data
	'''
	def __init__(self, data, prev_data_len = 0,
		a = 0x67452301,
		b = 0xEFCDAB89,
		c = 0x98BADCFE,
		d = 0x10325476,
		e = 0xC3D2E1F0):

		self.h = [a, b, c, d, e]
		print self.h
		self.data = data
		self.prev_data_len = prev_data_len
	
	@staticmethod
	def __ROTL(n, x, w=32):
		return ((x << n) | (x >> w - n))

	# Padding
	# All hashing are padded until the length is 8 bytes less than a full (64-byte) block
	# data + padding bytes 0x00(starting with 0x80) + 8 byte bit-length of data in big-endian
	def pre_process(self):
		ml = len(self.data) + self.prev_data_len
		#Append bit '1' 
		self.data = self.data.encode('hex') + '80'
		#Make len an multiple 0f 512 bits or 64 bytes
		l = (55-ml) % 64
		self.data = self.data + l*'00'

		#ml to 64-bit big-endian
		ml = hex(ml*8)[2:].rjust(16, '0')
		
		#Append bit-length of data
		self.data = self.data + ml
		self.data = self.data.decode('hex')


	# SHA1 is an iterating hashing algorithm
	# Each internal state depends on the previous one	
	def hash(self):
		MASK = 2**32-1
		self.pre_process()

		#break message into 512-bit(64 byte) block
		for i in range(0,len(self.data),64):
			block = self.data[i:i+64]
			#break block into sixteen 32-bit big-endian words
			w = [int(block[j:j+4].encode('hex'),16) for j in range(0, 64, 4)]
	
			for j in range(16,80):
				w.append(self.__ROTL(1, (w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16])) & MASK )
			
			#Initialize hash value for this block
			a, b, c, d, e = self.h[:]

			for j in range(80):
				if j in range(0, 20):
				    f = (b & c) ^ (~b & d)
				    k = 0x5A827999
				elif j in range(20, 40):
				    f = b ^ c ^ d
				    k = 0x6ED9EBA1
				elif j in range(40, 60):
				    f = (b & c) ^ (b & d) ^ (c & d)
				    k = 0x8F1BBCDC
				else :
				    f = b ^ c ^ d
				    k = 0xCA62C1D6

				temp = (self.__ROTL(5,a) + f + e + k + w[j]) & MASK
				e = d
				d = c
				c = self.__ROTL(30, b) & MASK
				b = a
				a = temp
				
		    #Add this block's hash to result so far:
			self.h[0] = (a + self.h[0]) & MASK
			self.h[1] = (b + self.h[1]) & MASK
			self.h[2] = (c + self.h[2]) & MASK
			self.h[3] = (d + self.h[3]) & MASK
			self.h[4] = (e + self.h[4]) & MASK
			
		#Produce the final hash value (big-endian) as a 160 bit number:
		hh = ''
		for h in self.h:
		    hh += (hex(h)[2:]).rjust(8, '0')
		return hh
		

if __name__ == '__main__':
	import sha

	print 'Input Message :',
	message = raw_input()
	key = 's3cr3tk5y'
	sha1_message = __SHA1(key + message).hash()
	print "SHA1(key || %s) = %s" % (repr(message), sha1_message)
	
	if (sha.new(key + message).hexdigest() == sha1_message):
		print '[+] Implementation Success'
