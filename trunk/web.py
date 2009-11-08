from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import os
import logging
import imdbParser

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write("""Welcome to IMDbotty's page !

More information maybe later... In the mean time, check http://code.google.com/p/imdbotty/ !""")

class FlushPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    if (memcache.flush_all()):
        self.response.out.write('Cache flushed !')
    else:
        self.response.out.write('Cannot flush cache...')

class GadgetPage(webapp.RequestHandler):
  def get(self):
    movieID = self.request.get('movieID')
    extension = self.request.get('ext')
    subdomain = self.request.get('sub')

    if extension == '':
        extension = 'com'
    
    if subdomain == '':
        subdomain = 'www'

    if movieID == '':
        movieID = '0133093' # Follow the white rabbit...

    cacheKey = '%s.%s.%s' % (subdomain, extension, movieID)

    movie = memcache.get(cacheKey)

    if movie is None:
        logging.debug('Movie %s not found in cache, downloading from IMDb...' % cacheKey)
        movie = imdbParser.IMDbParser(subdomain, extension, movieID)
        if not memcache.add(cacheKey, movie):
            logging.debug('Unable to add movie to the cache')
    else:
        logging.debug('Movie %s found in cache' % cacheKey)
    
    template_values = {
      'movie': movie
    }

    self.response.headers['Content-Type'] = 'text/xml'
    path = os.path.join(os.path.dirname(__file__), 'gadget.html')
    self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/gadget.xml', GadgetPage),
                                      ('/flush', FlushPage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
