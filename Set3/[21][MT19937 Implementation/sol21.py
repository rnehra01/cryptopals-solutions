
def _int32(x):
	return (0xFFFFFFFF & x)

class MT19937():
	"""MT19937 Implementation"""
	def __init__(self, seed):
		assert (int(seed)==seed)
		#Initialize the array
		self.index= 0
		self.MT   = [0]*624
		self.MT[0]= seed

		for i in range(1,624):
			self.MT[i]=_int32(1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> (32-2))) + i)

	def random(self):
		return self.extract_number()
	
	def extract_number(self):
		if (self.index==0):
			self.tempNumbers()
		
		y = self.MT[self.index]
		y = y ^ (y >> 11)
		y = y ^ ((y << 7) & 0x9d2c5680)
		y = y ^ ((y << 15) & 0xefc60000)
		y = y ^ (y >> 18)

		self.index = (self.index + 1) % 624
		return y

	def tempNumbers(self):
		'''Generate 624 tempered numbers'''
		for i in range(624):
		    # Get the most significant bit and add it to the less significant
		    # bits of the next number
		    y = _int32((self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff))
		    self.MT[i] = self.MT[(i + 397) % 624] ^ y >> 1

		    if y % 2 != 0:
		        self.MT[i] = self.MT[i] ^ 0x9908b0df

if __name__ == '__main__':
	m=MT19937(10)

	if (MT19937(10).random()==MT19937(10).random()):
		print '[+] Same SEED test passesd'

		