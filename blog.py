import os
import jinja2
import webapp2
import re
import json

from string import letters
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__) + "/templates")
jinja_env=jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
				autoescape=True)



class BaseHandler(webapp2.RequestHandler):
	def write(self,*a,**kw):
		self.response.out.write(*a,**kw)

	def render_str(self,template, **params):
        	t = jinja_env.get_template(template)
        	return t.render(params)

	def render(self,template,**kw):
        	self.response.out.write(self.render_str(template, **kw))



class Blog(db.Model):
	subject=db.StringProperty(required=True)
	content=db.StringProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)



class BlogHandler(BaseHandler):

	def render_blog(self):
		blogs=db.GqlQuery("SELECT * from Blog ORDER BY created DESC limit 10")
		self.render("blog.html",blogs=blogs)

	def get(self):
		self.render_blog()


	
class NewPostHandler(BaseHandler):

	def render_form(self,subject="",content="",subject_error="",content_error="",error=""):
		self.render("newpost.html",subject=subject,
					   content=content,
					   subject_error=subject_error,
					   content_error=content_error,
					   error=error)

	def get(self):
		self.render_form()

	def post(self):
		subject=self.request.get("subject")
		content=self.request.get("content")

		if subject and content:
			content=content.replace('\n' , '<br>')
			b=Blog(subject=subject,content=content)
			b.put()
			x=str(b.key().id())
			self.redirect('/blog/%s' % x)
			
			#self.write("Thanks for submitting your posts!!!!")

		elif subject and not content:
			self.render_form(subject=subject,content="",subject_error="",
						content_error="Please fill up the content page of the title!!!!!!!",error="")
		elif content and not subject:
			self.render_form(subject="",content=content,subject_error="Please fillup the title",
						content_error="",error="")
		else:
			self.render_form(subject="",content="",subject_error="",
						content_error="",error="Please fill up both the fields")



class PermalinkHandler(BaseHandler):
	
	def get(self,blog_id):
		
		blog=Blog.get_by_id(int(blog_id))
		if blog:
			self.render("permalink.html",blog=blog)
		
		self.error(404)

			
class BlogJson(BaseHandler):

	def get(self):
        	blogs = db.GqlQuery('SELECT * FROM Blog ORDER BY created DESC')
        	self.response.headers['content-type'] = 'application/json;utf-8'
        	list_json = []
        	for blog in blogs:
        	    dict_json = {}
        	    dict_json['content'] = blog.content
        	    dict_json['subject'] = blog.subject
        	    list_json.append(dict_json)
        	self.write(json.dumps(list_json))
			

class PermJson(BaseHandler):

	def get(self,blog_id):
		blog=Blog.get_by_id(int(blog_id))
		if blog:
			self.response.headers['content-type'] = 'application/json;utf-8'
			list_json=[]
			dict_json={}
			dict_json['content']=blog.content
			dict_json['subject']=blog.subject
			list_json.append(dict_json)
			self.write(json.dumps(list_json))
		self.error(404)
		

app=webapp2.WSGIApplication([('/blog' , BlogHandler),
			     ('/blog/newpost' , NewPostHandler),
			     ('/blog/([0-9]+)' , PermalinkHandler),
			     ('/blog.json' , BlogJson),
			     ('/blog/([0-9]+).json' , PermJson)],
				debug = True)

