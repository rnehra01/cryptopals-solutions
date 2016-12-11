import time
from PRNG import MT19937
from random import randint

def get_random_number():
	time.sleep(randint(40,100))
	seed=int(time.time())
	m=MT19937(seed)
	print 'Used seed : '+str(seed)
	time.sleep(randint(40,100))
	return m.random()

def crack_seed(random_no):
	possible_seeds=[]
	cur_time=int(time.time())
	for x in range(cur_time-200,cur_time+1):
		if MT19937(x).random() == random_no :
			possible_seeds.append(x)
	return possible_seeds

if __name__ == '__main__':
	
	seeds=crack_seed(get_random_number())
	if(len(seeds)):
		print '[+] Cracked :'+seeds 