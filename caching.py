import time

def complex_computation(a,b):
	time.sleep(.5)
	return a+b

cache = {}

def cache_computation(a,b):
	key = (a,b)
	if key in cache:
		r=cache[key]
	else:
		r=complex_computation(a,b)
		cache[key]=r
	return r

print cache_computation(3,5)

start_time1=time.time()

print "The first computation took %f seconds" % (time.time() - start_time1)


print cache_computation(3,5)

start_time1=time.time()

print "The second computation took %f seconds" % (time.time() - start_time1)

 
