import os

import webapp2
import jinja2
import json


template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class BaseHandler(webapp2.RequestHandler):
    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self,template,**kw):
        self.response.write(self.render_str(template, **kw))
    def write(self,*a,**kw):
        self.response.write(*a, **kw)

class MainPage(BaseHandler):
	def get(self):
		self.render('home.html',username="")

class FormPage(BaseHandler):
    def write_form(self,error='',month='',day='',year=''):
        self.render('formcheck.html',error=error,day=day,year=year,month=month)

    def get(self):
        self.render('formcheck.html')
   
    def post(self): #when we post our form
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        year = valid_year(user_year)
        day = valid_day(user_day)
        if not(month and year and day):
            self.write_form(error="You cannot even enter dates properly. Shame one you..",
                            day=user_day,
                            month=user_month,
                            year=user_year)
        else:
            self.redirect('/thanks')      

class ThanksHandler(BaseHandler):
    def get(self):
        self.write('<b>You are awesome!</b>')






app = webapp2.WSGIApplication([ ('/',MainPage), 
								('/forms',FormPage),
								('/thanks',ThanksHandler)
								
                                
                               ],
								debug=True)

