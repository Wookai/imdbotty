import re
import urllib

class IMDbParser:
    tvSeriesPattern = '<span class="tv-extra">TV series</span>'
    titlePattern = re.compile('<div id="tn15title">\s+<h1>(?P<title>[^<]+)\s+<span>\(<a[^>]+>(?P<year>\d+)</a>[^)]*\)')
    coverPattern = re.compile('<div class="photo">\s+<a[^>]+><img[^>]+src="(?P<coverURL>http://[^"]+)"[^>]+></a>')
    ratingPattern = re.compile('<div class="meta">\s+<b>(?P<rating>[\d\.]+/10)</b>')
    directorsPattern = re.compile('<div[^>]*id="director-info"[^>]*>\s+<h5>[^<]+</h5>\s+(?P<directors>(<a[^>]+>([^<]+)</a><br/>\s+)+)</div>')
    directorsSubpattern = re.compile('<a[^>]+>(?P<name>[^<]+)</a>')
    creatorsPattern = re.compile('<div class="info">\s+<h5>Creators:</h5>\s+(?P<creators>(<a[^>]+>([^<]+)</a><br/>\s+)+)</div>')
    creatorsSubpattern = re.compile('<a[^>]+onclick="[^>]+>(?P<name>[^<]+)</a>')
    actorPattern = re.compile('<td class="nm"><a[^>]+>(?P<name>[^<]+)</a></td>')

    def __init__(self, movieID):
        """ Parses data from a movie/tv show on IMDb """
        self.url = 'http://www.imdb.com/title/tt' + movieID

        self.title, self.year, self.coverURL, self.rating = '', '', '', ''
        self.creators, self.directors, self.actors = [], [], []
        
        self.parseData()

    def parseData(self):
        html = urllib.urlopen(self.url).read()

        self.isTvSerie = (html.find(self.tvSeriesPattern) > -1)

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
            self.ratingInt = int(self.rating.replace('/10', '').replace('.', ''))

        if self.isTvSerie:
            # parse creators
            creators = self.creatorsPattern.search(html)

            if creators is None:
                self.creators.append('N/A')
            else:
                creators = creators.group('creators')
                for c in self.creatorsSubpattern.finditer(creators):
                    self.creators.append(c.group('name'))
        else:
            # parse directors
            directors = self.directorsPattern.search(html)

            if directors is None:
                self.directors.append('N/A')
            else:
                directors = directors.group('directors')
                for d in self.directorsSubpattern.finditer(directors):
                    self.directors.append(d.group('name'))

        # parse actors
        nbActorsMax = 6
        i = 1
        for a in self.actorPattern.finditer(html):
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
        
