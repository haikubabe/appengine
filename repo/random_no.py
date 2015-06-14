import random
from string import letters
import hashlib



def make_salt():
    return ''.join(random.choice(string.letters) for i in xrange(5))
    ###Your code here
#make_salt()   

def make_pw_hash(name,pw,salt=None):
	if not salt:
		salt=make_salt()
	h=hashlib.sha256(name+pw+salt).hexdigest()
	return '%s%s' % (h,salt)	


def valid_pw(name,pw,h):
	salt=h.split(',')[1]
	return h==make_pw_hash(name,pw,salt)
		

h = make_pw_hash('sourav','gosour94')
print h
print valid_pw('sourav','gosour94',h) 


