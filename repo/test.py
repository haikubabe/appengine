import os

import jinja2
import webapp2

template_dir=os.path.join(os.path.dirname(__file__) + "/templates")
jinja_env=jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))


class BaseHandler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template, **params):
        	t = jinja_env.get_template(template)
        	return t.render(params)

	def render(self,template,**kw):
        	self.response.out.write(self.render_str(template, **kw))


class ShoppingHandler(BaseHandler):
	def get(self):

		items=self.request.get_all("food")			
		self.render('shopping.html',items=items)


class GosourHandler(BaseHandler):
	def get(self):
		n=self.request.get('n',0)

		if n:
			n = int(n)
			
		self.render('hello_gosour.html', n=n)


class FizzBuzzHandler(BaseHandler):
	def get(self):
		n=self.request.get('n' , 0)
		if n:
			n=int(n)
		self.render('fizzbuz.html',n=n)
		

app=webapp2.WSGIApplication([('/shopping' , ShoppingHandler),
				('/gosour' , GosourHandler),
				('/fizzbuz' , FizzBuzzHandler)],
					debug = True)


