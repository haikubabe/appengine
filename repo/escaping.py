import cgi

def escape_fun(s):
	h=cgi.escape(s,quote=True)
	return h

print escape_fun('">=<&html>amp"')
