import os
import jinja2
import webapp2
import urllib2

from xml.dom import minidom
from google.appengine.ext import db

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



GMAPS_URL = "https://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def gmaps_img(points):
        markers = '&'.join('markers=%s,%s' % (p.lat,p.lon) for p in points)
        return GMAPS_URL + markers



IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
	#ip = "4.2.2.2"
	ip = "23.24.209.141"
	url = IP_URL + ip
	content = None  					# store the content of the url in a variable named content
	try:
		content=urllib2.urlopen(url).read()
	
	except urllib2.URLError:
		return

	if content:

		#parse the xml content and find the coordinates
		d = minidom.parseString(content)
		coords = d.getElementsByTagName("gml:coordinates")
		if coords and coords[0].childNodes[0].nodeValue:
			lon,lat = coords[0].childNodes[0].nodeValue.split(',')
			return db.GeoPt(lat,lon)	 # GeoPt is a datatype for storing latitude & longitude


class Art(db.Model):				
	
	#class Art inherit from db.model class, this class(Art) helps to create the entity of a database	
	title=db.StringProperty(required=True)
	art=db.TextProperty(required=True)
	created=db.DateTimeProperty(auto_now_add=True)
	coords=db.GeoPtProperty()


class MainPage(BaseHandler):

	def render_front(self,title="",art="",error=""):
		arts=db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")

		# prevent the running of multiple queries
		arts=list(arts)				

		# find which arts have coordinates
		points = []
		for a in arts:
			if a.coords:
				points.append(a.coords)
		
		#points=filter(None, (a.coords for a in arts))

		#self.write(repr(points))

		# if we have any arts coord then make the image url
		img_url = None

		if points:
			img_url = gmaps_img(points)

		
		#display the image url
		self.render("ascii.html",title=title,art=art,error=error,arts=arts,img_url=img_url)	

	
	def get(self):


		self.write(self.request.remote_addr)
		self.write(repr(get_coords(self.request.remote_addr)))
		self.render_front()

	
	def post(self):
		title=self.request.get("title")
		art=self.request.get("art")

		if title and art:

			#an instance of Art is created 			
			a=Art(title=title,art=art)				

			#lookup the users coordinate from their IP
			coords = get_coords(self.request.remote_addr)
			#if we have the coordinates then we add them to the Art
			if coords:    	
				a.coords = coords					

			#this will store the new art object a into the database
			a.put()							
			self.redirect("/")
		else:
			error="Please don't left the fields blank we need both your thoughts (title and art)"
			self.render_front(title,art,error)


app=webapp2.WSGIApplication([('/' , MainPage)],
				debug = True)

