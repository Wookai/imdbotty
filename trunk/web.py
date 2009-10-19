from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import os
import urllib
import re

titlePattern = re.compile('<div id="tn15title">\s+<h1>(?P<title>[^<]+)\s+<span>\(<a[^>]+>(?P<year>\d+)</a>\)')
coverPattern = re.compile('<div class="photo">\s+<a[^>]+name="poster"[^>]+><img[^>]+src="(?P<coverURL>http://[^"]+)"[^>]+></a>')
ratingPattern = re.compile('<div class="meta">\s+<b>(?P<rating>[\d\.]+/10)</b>')
directorsPattern = re.compile('<div[^>]*id="director-info"[^>]*>\s+<h5>[^<]+</h5>\s+(?P<directors>(<a[^>]+>([^<]+)</a><br/>\s+)+)</div>')
directorsSubpattern = re.compile('<a[^>]+>(?P<name>[^<]+)</a>')
actorPattern = re.compile('<td class="nm"><a[^>]+>(?P<name>[^<]+)</a></td>')

class IMDbMovie:
    def __init__(self, movieID):
        self.url = 'http://www.imdb.com/title/tt' + movieID

        self.title, self.year, self.coverURL, self.rating = '', '', '', ''
        self.directors, self.actors = [], []
        
        self.parseData()

    def parseData(self):
        html = urllib.urlopen(self.url).read()

        # parse title and year
        m = titlePattern.search(html)
        self.title, self.year = m.group('title'), m.group('year')

        # parse cover URL
        m = coverPattern.search(html)
        self.coverURL = m.group('coverURL')

        # parse rating
        m = ratingPattern.search(html)
        self.rating = m.group('rating')
        self.ratingInt = int(self.rating.replace('/10', '').replace('.', ''))

        # parse directors
        directors = directorsPattern.search(html).group('directors')
        for d in directorsSubpattern.finditer(directors):
            self.directors.append(d.group('name'))

        # parse actors
        nbActorsMax = 6
        i = 1
        for a in actorPattern.finditer(html):
            if i > nbActorsMax:
                break
            self.actors.append(a.group('name'))
            i = i + 1

    def __str__(self):
        print 'Title:', self.title
        print 'Year:', self.year
        print 'URL:', self.url
        print 'Cover URL:', self.coverURL
        print 'Rating:', self.rating
        print 'Director(s):'
        for d in self.directors:
            print '', d
        print 'Actors:'
        for a in self.actors:
            print '', a

class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Welcome to IMDbotty\'s page !\n\nMore information maybe later...')

class GadgetPage(webapp.RequestHandler):
  def get(self):
    movieID = self.request.get('movieID')

    movie = IMDbMovie(movieID)
    
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
