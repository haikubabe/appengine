import hmac

SECRET='imsosecret'

def hash_str(s):
	return hmac.new(SECRET,s).hexdigest()

