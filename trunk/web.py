from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import os
import imdbParser

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""Welcome to IMDbotty's page !

More information maybe later... In the mean time, check http://code.google.com/p/imdbotty/ !""")

class GadgetPage(webapp.RequestHandler):
  def get(self):
    movieID = self.request.get('movieID')

    if movieID == '':
        movieID = '0133093' # Follow the white rabbit...

    movie = memcache.get(movieID)

    if movie is None:
        movie = imdbParser.IMDbParser(movieID)
        memcache.add(movieID, movie, 3600*24*30) # expires in 30 days
    
    template_values = {
      'movie': movie
    }

    self.response.headers['Content-Type'] = 'text/xml'
    path = os.path.join(os.path.dirname(__file__), 'gadget.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/gadget.xml', GadgetPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
