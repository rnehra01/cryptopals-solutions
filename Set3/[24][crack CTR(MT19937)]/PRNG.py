
def _int32(x):
	return (0xFFFFFFFF & x)

class MT19937():
	"""MT19937 Implementation"""
	def __init__(self, seed):
		self.index= 0
		self.MT   = [0]*624
		if (type(seed)==int):
			self.MT[0]= seed
			for i in range(1,624):
				self.MT[i]=_int32(1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> (32-2))) + i)
		elif (type(seed)==list and len(seed)==624):
			self.MT = seed
		else :
			raise Exception

	def random(self):
		return self.extract_number()
	
	def extract_number(self):
		if (self.index==0):
			self.randomize()
			
		y = self.temper(self.MT[self.index])

		self.index = (self.index + 1) % 624
		return y

	@staticmethod
	def temper(value):
		y = value
		y = y ^ (y >> 11)
		y = y ^ ((y << 7) & 0x9d2c5680)
		y = y ^ ((y << 15) & 0xefc60000)
		y = y ^ (y >> 18)
		return y

	@staticmethod
	def untemper(y):
		# Reverse y = y ^ (y >> 18)
		y = y ^ (y >> 18)
		# Reverse y = y ^ ((y << 15) & 0xefc60000)
		y = y ^ ((y << 15) & 0xefc60000)
		# Reverse y = y ^ ((y << 7) & 0x9d2c5680)
		a = y & 0x0000007f												# last 7 bits
		b = (((a<<7) & 0x9d2c5680) ^ y) & 0x00003f80					# next 7 bits
		c = (((b<<7) & 0x9d2c5680) ^ y) & 0x001fc000					# next 7 bits
		d = (((c<<7) & 0x9d2c5680) ^ y) & 0x0fe00000					# next 7 bits
		e = (((d<<7) & 0x9d2c5680) ^ y) & 0xf0000000					# first 4 bits
		y = a | b | c | d | e
		# Reverse y = y ^ (y >> 11)
		a = y & 0xffe00000												# first 11 bits
		b = ((a>>11) ^ y) & 0x001ffc00									# next 11 bits
		c = (((b & 0x001ff800)>>11) ^ y) & 0x000003ff					# last 10 bits
		value = a | b | c
		return value

	def randomize(self):
		'''Generate 624 tempered numbers'''
		for i in range(624):
		    # Get the most significant bit and add it to the less significant
		    # bits of the next number
		    y = (self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)
		    self.MT[i] = self.MT[(i + 397) % 624] ^ y >> 1

		    if y % 2 != 0:
		        self.MT[i] = self.MT[i] ^ 0x9908b0df