import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template=JINJA_ENVIRONMENT.get_template('hello_gosour.html')
		self.response.out.write(template.render())

app=webapp2.WSGIApplication([('/' , MainPage)],
					debug = True)
