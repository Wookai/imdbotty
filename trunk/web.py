from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

import os
import urllib
import re

tvSeriesPattern = '<span class="tv-extra">TV series</span>'
titlePattern = re.compile('<div id="tn15title">\s+<h1>(?P<title>[^<]+)\s+<span>\(<a[^>]+>(?P<year>\d+)</a>\)')
coverPattern = re.compile('<div class="photo">\s+<a[^>]+><img[^>]+src="(?P<coverURL>http://[^"]+)"[^>]+></a>')
ratingPattern = re.compile('<div class="meta">\s+<b>(?P<rating>[\d\.]+/10)</b>')
directorsPattern = re.compile('<div[^>]*id="director-info"[^>]*>\s+<h5>[^<]+</h5>\s+(?P<directors>(<a[^>]+>([^<]+)</a><br/>\s+)+)</div>')
directorsSubpattern = re.compile('<a[^>]+>(?P<name>[^<]+)</a>')
creatorsPattern = re.compile('<div class="info">\s+<h5>Creators:</h5>\s+(?P<creators>(<a[^>]+>([^<]+)</a><br/>\s+)+)</div>')
creatorsSubpattern = re.compile('<a[^>]+onclick="[^>]+>(?P<name>[^<]+)</a>')
actorPattern = re.compile('<td class="nm"><a[^>]+>(?P<name>[^<]+)</a></td>')

class IMDbMovie:
    def __init__(self, movieID):
        self.url = 'http://www.imdb.com/title/tt' + movieID

        self.title, self.year, self.coverURL, self.rating = '', '', '', ''
        self.creators, self.directors, self.actors = [], [], []
        
        self.parseData()

    def parseData(self):
        html = urllib.urlopen(self.url).read()

        self.isTvSerie = (html.find(tvSeriesPattern) > -1)

        # parse title and year
        m = titlePattern.search(html)
        self.title, self.year = m.group('title'), m.group('year')

        # parse cover URL
        m = coverPattern.search(html)
        self.coverURL = m.group('coverURL')

        # parse rating
        m = ratingPattern.search(html)
        if m is None:
            self.rating = 'N/A'
            self.ratingInt = 0
        else:
            self.rating = m.group('rating')
            self.ratingInt = int(self.rating.replace('/10', '').replace('.', ''))

        if self.isTvSerie:
            # parse creators
            creators = creatorsPattern.search(html)

            if creators is None:
                self.creators.append('N/A')
            else:
                creators = creators.group('creators')
                for c in creatorsSubpattern.finditer(creators):
                    self.creators.append(c.group('name'))
        else:
            # parse directors
            directors = directorsPattern.search(html)

            if directors is None:
                self.directors.append('N/A')
            else:
                directors = directors.group('directors')
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
        print 'TvSerie:', self.isTvSerie
        print 'Year:', self.year
        print 'URL:', self.url
        print 'Cover URL:', self.coverURL
        print 'Rating:', self.rating
        if self.isTvSerie:
            print 'Creator(s):'
            for c in self.creators:
                print '', c
        else:
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

    if movieID == '':
        movieID = '0133093' # Follow the white rabbit...

    movie = memcache.get(movieID)

    if movie is None:
        movie = IMDbMovie(movieID)
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
