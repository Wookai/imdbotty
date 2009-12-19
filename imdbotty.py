from waveapi import events
from waveapi import model
from waveapi import robot
from waveapi import document

import logging
import re

imdbLinkPattern = re.compile('(http://)?(?P<sub>www|uk).imdb.(?P<ext>\w{2,3})/title/tt(?P<movieID>\d{7})(/)?')

def OnRobotAdded(properties, context):
    logging.debug('Bot added to a wave')
    root_wavelet = context.GetRootWavelet()
    root_wavelet.CreateBlip().GetDocument().SetText("Thanks for adding me ! To use me, simply add a URL to a movie on IMDB.")


def OnDocumentChanged(properties, context):
    blip = context.GetBlipById(properties['blipId'])
    doc = blip.GetDocument()

    # find all urls
    urls = []
    for url in imdbLinkPattern.finditer(doc.GetText()):
        logging.debug('Found IMDb url %s (movie ID %s)' % (url.group(0), url.group('movieID')))
        urls.append(url)

    # reverse array to replace matches from the last one to the first one
    # (this way, the starts and ends of matches are still valid)
    urls.reverse()

    # do the actual replacement
    for url in urls:
        imdbID = url.group('movieID')
        sub = url.group('sub')
        ext = url.group('ext')
        gadgetUrl = 'http://imdbotty.appspot.com/gadget.xml?sub=%s&ext=%s&movieID=%s' % (sub, ext, imdbID)
    
        logging.debug('Inserting gadget with url %s' % gadgetUrl)
        
        doc.DeleteRange(document.Range(url.start(), url.end()))
        gadget = document.Gadget(gadgetUrl)
        doc.InsertElement(url.start(), gadget)


if __name__ == '__main__':
    myRobot = robot.Robot('IMDbotty',
      image_url='http://imdbotty.appspot.com/assets/imdbotty.png',
      version='1.5.2',
      profile_url='http://imdbotty.appspot.com/')
    myRobot.RegisterHandler(events.DOCUMENT_CHANGED, OnDocumentChanged)
    myRobot.RegisterHandler(events.WAVELET_SELF_ADDED, OnRobotAdded)
    myRobot.Run()

