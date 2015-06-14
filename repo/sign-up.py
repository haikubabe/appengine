import os
import re
import webapp2
import jinja2
import hashlib
import hmac
import random

from rot13 import translate
from string import letters
from google.appengine.ext import db


SECRET='doyouwantsomecookie'


template_dir=os.path.join(os.path.dirname(__file__) + "/templates")
jinja_env=jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
				autoescape=True)



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
  
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
  
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)



# For generating hash of a string

def hash_str(name):
	return hmac.new(SECRET,name).hexdigest()


# For setting a cookie (i.e. for sending a cookie to the user)

def set_secure_cookie(name):
	return '%s|%s' % (name,hash_str(name))

def check_secure_cookie(h):
	name=h.split('|')[0]
	if h==set_secure_cookie(name):
		return name



class BaseHandler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template, **params):
        	t = jinja_env.get_template(template)
        	return t.render(params)

	def render(self,template,**kw):
        	self.response.out.write(self.render_str(template, **kw))



class User(db.Model):
	username=db.StringProperty(required=True)
	password=db.StringProperty(required=True)
	email=db.StringProperty()


class Rot13Handler(BaseHandler):
	
	def get(self):
		self.render("rot13.html")

	def post(self):

		new_text=self.request.get("text")
		trans_text=translate(new_text)
		self.render("rot13.html",text=trans_text)


class SignUpHandler(BaseHandler):
	
	def get(self):
		self.render('sign-up.html')

	def post(self):

		error=False

	
		username=self.request.get('username')
		password=self.request.get('password')
		verify=self.request.get('verify')
		email=self.request.get('email')
	
		params = dict(username=username , password=password , verify=verify , email=email)

		if not valid_username(username):
			params['error_username'] = "That's not a valid username!"
			error=True
		if not valid_password(password):
			params['error_password'] = "Invalid password!"
			error=True
		elif password!=verify:
			params['error_verify'] = "Password didn't match!"
			error=True
		if not valid_email(email):
			params['error_email'] = "That's not a valid email address!"
			error=True

		if error:
			self.render('sign-up.html',**params)
		else:
			
			self.redirect('/unit-2/welcome?username=' + username)


class Registration(BaseHandler):
			
	def get(self):
		self.render('sign-up.html')

	def post(self):

		error=False
		have_error=""
	
		username=self.request.get('username')
		password=self.request.get('password')
		verify=self.request.get('verify')
		email=self.request.get('email')
	
		params = dict(username=username , password=password , verify=verify , email=email , have_error=have_error)

		if not valid_username(username):
			params['error_username'] = "That's not a valid username!"
			error=True
		if not valid_password(password):
			params['error_password'] = "Invalid password!"
			error=True
		elif password!=verify:
			params['error_verify'] = "Password didn't match!"
			error=True
		if not valid_email(email):
			params['error_email'] = "That's not a valid email address!"
			error=True

		usernames = db.GqlQuery("SELECT * FROM User WHERE username = \'%s\'" % (username))
		user=usernames.get()

		if user:
			params['have_error'] = "That username already exists!!!!"
			error=True
		else:
			error=False

		if error==True:
			self.render('sign-up.html',**params)
		else:
			u=User(username=username,password=password,email=email)
			u.put()
			cookie = 'username=%s ; Path=/' % (set_secure_cookie(username))
			self.response.headers.add_header('Set-Cookie' , cookie.encode('ascii'))   
			self.redirect('/unit-3/welcome')


class Welcome(BaseHandler):
	
	def get(self):
		cookie_str=self.request.cookies.get('username')		# to get a cookie from the user (from browser to server)
		username=check_secure_cookie(cookie_str)
		if valid_username(username):
			self.render('welcome.html' , username=username)
		else:
			self.redirect('/unit-3/signup')


class WelcomeHandler(BaseHandler):
	
	def get(self):
		username=self.request.get('username')
		if valid_username(username):
			self.render('welcome.html',username=username)
		else:
			self.redirect('/unit-2/signup')


class Login(BaseHandler):
	
	def get(self):
		self.render('login.html')
	
	def post(self):
		username=self.request.get('username')
		password=self.request.get('password')
		
		#user_pass=db.GqlQuery("SELECT * FROM User WHERE username=:1 AND password=:1", username,password)
		user_pass = db.GqlQuery("SELECT * FROM User WHERE username = \'%s\' AND password = \'%s\'" % (username,password))
		result = user_pass.get()
		error = "Invalid Login"

				
		if not result:
			self.render("login.html",error=error,username=username)
		else:
			cookie='username=%s ; Path=/' % (set_secure_cookie(username))
			self.response.headers.add_header("Set-Cookie" , cookie.encode('ascii'))
			self.redirect('/unit-3/welcome')


class Logout(BaseHandler):
	def get(self):
		self.response.headers.add_header('Set-Cookie' , 'username= ; Path=/')
		self.redirect('/unit-3/signup')			



class MainPage(BaseHandler):
	def get(self):
		self.write("Helloooooooo Welcome Welcome Welcome!!!!!")
		#self.render("hello.html")


app = webapp2.WSGIApplication([
    ('/' , MainPage),
    ('/unit-2/rot13' , Rot13Handler),
    ('/unit-2/signup' , SignUpHandler),
    ('/unit-2/welcome' , WelcomeHandler),
    ('/unit-3/signup' , Registration), 
    ('/unit-3/welcome' , Welcome),
    ('/unit-3/login' , Login),
    ('/unit-3/logout' , Logout)],debug=True)




