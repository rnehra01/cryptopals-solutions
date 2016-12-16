
class __SHA1():
	"""SHA1 implementation"""
	def __init__(self, data):
		self.h = [
            0x67452301,
            0xEFCDAB89,
            0x98BADCFE,
            0x10325476,
            0xC3D2E1F0
            ]
		self.data = data
	
	@staticmethod
	def __ROTL(n, x, w=32):
		return ((x << n) | (x >> w - n))

	def pre_process(self):
		ml = len(self.data)
		#Append bit '1' 
		self.data = self.data.encode('hex') + '80'
		#Make len an multiple 0f 512 bits or 64 bytes
		l = (55-ml) % 64
		self.data = self.data + l*'00'

		#ml to 64-bit big-endian
		ml = hex(ml*8)[2:]
		ml = '0'*(16-len(ml)%16) + ml
		#Append +4-bit length
		self.data = self.data + ml
		self.data = self.data.decode('hex')
		
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

	print 'Input Message :',
	message = raw_input()
	key = 's3cr3tk5y'
	print "SHA1(key || %s) = %s" % (repr(message), __SHA1(key + message).hash())
	
