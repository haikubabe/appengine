import hashlib

def hash_str(s):
	return hashlib.md5(s).hexdigest()

def make_secure_val(s):
	return "%s,%s" %(s,hash_str(s))

def check_secure_val(h):
	val=h.split(',')[0]
	if h==make_secure_val(val):
		return val

print check_secure_val("cool,b1f4f9a523e36fd969f4573e25af4540")
