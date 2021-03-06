import os

import webapp2
import jinja2
import json
import valid_day
import valid_year
import valid
from escaping import escape_fun


template_dir=os.path.join(os.path.dirname(_file_),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)


def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)


class BaseHandler(webapp2.RequestHandler):
    
    def render(self,template,**kw):
        self.response.out.write(render_str(template, **kw))
    def write(self,*a,**kw):
        self.response.out.write(*a, **kw)

class MainPage(BaseHandler):
    
    def write_form(self,error="",month="",day="",year=""):
		self.render('birthday.html',error=error,month=month,day=day,year=year)
	    

    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.render('birthday.html')

    def post(self):
		user_month=self.request.get('month')
		user_day=self.request.get('day')
		user_year=self.request.get('year')

		month=valid.valid_month(self.request.get('month'))
		day=valid_day.valid_day(self.request.get('day'))
		year=valid_year.valid_year(self.request.get('year'))		
	
		if not (month and day and year):
			self.write_form("Not a valid date!",user_month,user_day,user_year)
		else:
			self.redirect("/thanks")


class Thankshandler(BaseHandler):
	
	def get(self):
		self.write("Thanks! That's a valid date!")


app = webapp2.WSGIApplication([
    ('/', MainPage),('/thanks', Thankshandler)],debug=True)

