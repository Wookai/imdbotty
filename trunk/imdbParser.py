from google.appengine.api import urlfetch

import re
import logging

class IMDbPerson:
    def __init__(self, name, url):
        self.url = url
        self.name = name
    
    def __str__(self):
        return self.name + '\t' + self.url

class IMDbParser:
    tvSeriesPattern = re.compile('<span class="tv-extra">[^<]*TV[^<]*</span>')
    titlePattern = re.compile('<div id="tn15title">\s+<h1>(?P<title>[^<]+)\s+<span>\((<a[^>]+>)?(?P<year>\d+)(</a>)?[^)]*\)')
    coverPattern = re.compile('<div class="photo">\s+<a[^>]+><img[^>]+src="(?P<coverURL>http://[^"]+)"[^>]+></a>')
    ratingPattern = re.compile('<div class="starbar-meta">\s+<b>(?P<rating>[\d\.,]+/10)</b>')
    directorsPattern = re.compile('<div[^>]*id="director-info"[^>]*>\s+<h5>(?P<label>[^<]*)</h5>\s+<div class="info-content">\s+(?P<directors>(<a[^>]+>([^<]+)</a>[^<]*<br/>\s+)+)</div>\s+</div>')
    directorsSubpattern = re.compile('<a[^>]+href="(?P<url>[^"]+)"[^>]*>(?P<name>[^<]+)</a>')
    creatorsPattern = re.compile('<div class="info">\s+<h5>(?P<label>[^<]*)</h5>\s+<div class="info-content">\s+(?P<creators>(<a[^>]+>([^<]+)</a>[^<]*<br/>\s+)+)')
    creatorsSubpattern = re.compile('<a href="(?P<url>[^"]+)" onclick="[^"]*">(?P<name>[^<]+)</a>')
    actorsLabelPattern = re.compile('<div class="headerinline"><h3>(?P<label>[^>]+)</h3>')
    actorPattern = re.compile('<td class="nm"><a[^>]*href="(?P<url>[^"]+)"[^>]*>(?P<name>[^<]+)</a></td>')

    def __init__(self, subdomain, extension, movieID):
        """ Parses data from a movie/tv show on IMDb """
        self.subdomain = subdomain
        self.extension = extension
        self.movieID = movieID
        self.url = 'http://%s.imdb.%s/title/tt%s' % (subdomain, extension, movieID)

        # default values in case we can't parse the page
        self.title, self.year, self.coverURL, self.rating = 'N/A', 'N/A', 'http://img407.imageshack.us/img407/6493/titleaddposterw.jpg', 'N/A'
        self.ratingInt = 0
        self.creators, self.directors, self.actors = [], [], []
        self.creatorsLabel, self.directorsLabel, self.actorsLabel = 'Creator(s)', 'Director(s)', 'Actors'
        
        self.parseData()

    def parseData(self):
        html = ''
        nbAttemptsMax = 5
        nbAttempts = 0
        found = False
        
        # try to download the page several times
        while not found and nbAttempts < nbAttemptsMax:
            # sometimes urlopen raises an exception, so retry instead of fail
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.1) Gecko/20100122 firefox/3.6.1'}
                response =  urlfetch.fetch(url=self.url,
                                       headers=headers)
                html = response.content
                found = (self.titlePattern.search(html) is not None)
            except:
                pass
            nbAttempts = nbAttempts + 1
        
        if not found:
            logging.warn('Unable to get html content after %s attempts...' % nbAttemptsMax)
            return

        self.isTvSerie = self.tvSeriesPattern.search(html) is not None
        logging.debug('Is this a TV show ? ' + str(self.isTvSerie))

        # parse title and year
        m = self.titlePattern.search(html)
        self.title, self.year = m.group('title'), m.group('year')

        # parse cover URL
        m = self.coverPattern.search(html)
        self.coverURL = m.group('coverURL')

        # parse rating
        m = self.ratingPattern.search(html)
        if m is None:
            self.rating = 'N/A'
            self.ratingInt = 0
        else:
            self.rating = m.group('rating')
            self.ratingInt = int(self.rating.replace('/10', '').replace('.', '').replace(',', ''))

        if self.isTvSerie:
            # parse creators
            creators = self.creatorsPattern.search(html)

            if creators is None:
                self.creators.append(IMDbPerson('N/A', ''))
            else:
                self.creatorsLabel = creators.group('label')
                creators = creators.group('creators')
                for c in self.creatorsSubpattern.finditer(creators):
                    self.creators.append(IMDbPerson(c.group('name'), c.group('url')))
        else:
            # parse directors
            directors = self.directorsPattern.search(html)

            if directors is None:
                self.directors.append(IMDbPerson('N/A', ''))
            else:
                self.directorsLabel = directors.group('label')
                directors = directors.group('directors')
                for d in self.directorsSubpattern.finditer(directors):
                    self.directors.append(IMDbPerson(d.group('name'), d.group('url')))

        # parse actors
        self.actorsLabel = self.actorsLabelPattern.search(html).group('label') + ':'
        nbActorsMax = 6
        i = 1
        for a in self.actorPattern.finditer(html):
            if i > nbActorsMax:
                break
            self.actors.append(IMDbPerson(a.group('name'), a.group('url')))
            i = i + 1

    def __str__(self):
        print 'Title:', self.title
        print 'TvSerie:', self.isTvSerie
        print 'Year:', self.year
        print 'URL:', self.url
        print 'Cover URL:', self.coverURL
        print 'Rating:', self.rating
        if self.isTvSerie:
            print self.creatorsLabel
            for c in self.creators:
                print '', c
        else:
            print self.directorsLabel
            for d in self.directors:
                print '', d
        print self.actorsLabel
        for a in self.actors:
            print '', a
        return ''