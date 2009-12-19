# -*- coding: utf-8 -*-

import unittest
import imdbParser

class TestImdbParserMovie(unittest.TestCase):

    def _checkGlobalData(self, m):
        self.assertEquals(m.year, '2009')
        self.assertFalse(m.isTvSerie)
        self.assertEquals(len(m.directors), 1)
        self.assertEquals(m.directors[0].name, 'Quentin Tarantino')
        self.assertEquals(m.directors[0].url, '/name/nm0000233/')
        self.assertEquals(len(m.creators), 0)
        self.assertEquals(len(m.actors), 6)
        self.assertEquals(m.actors[0].name, 'Brad Pitt')
        self.assertEquals(m.actors[0].url, '/name/nm0000093/')
        self.assertEquals(m.actors[1].name, 'M&#xE9;lanie Laurent')
        self.assertEquals(m.actors[1].url, '/name/nm0491259/')
        
    def testCom(self):
        m = imdbParser.IMDbParser('www', 'com', '0361748')
        self._checkGlobalData(m)
        self.assertEquals(m.title, 'Inglourious Basterds')
        self.assertEquals(m.directorsLabel, 'Director:')
        self.assertEquals(m.actorsLabel, 'Cast:')
        
    def testUk(self):
        m = imdbParser.IMDbParser('uk', 'com', '0361748')
        self._checkGlobalData(m)
        self.assertEquals(m.title, 'Inglourious Basterds')
        self.assertEquals(m.directorsLabel, 'Director:')
        self.assertEquals(m.actorsLabel, 'Cast:')

    def testFr(self):
        m = imdbParser.IMDbParser('www', 'fr', '0361748')
        self._checkGlobalData(m)
        self.assertEquals(m.title, 'Inglourious Basterds')
        self.assertEquals(m.directorsLabel, 'R&#xE9;alisateur:')
        self.assertEquals(m.actorsLabel, 'Ensemble:')

    def testDe(self):
        m = imdbParser.IMDbParser('www', 'de', '0361748')
        self._checkGlobalData(m)
        self.assertEquals(m.title, 'Inglourious Basterds')
        self.assertEquals(m.directorsLabel, 'Regisseur:')
        self.assertEquals(m.actorsLabel, 'Besetzung:')

    def testIt(self):
        m = imdbParser.IMDbParser('www', 'it', '0361748')
        self._checkGlobalData(m)
        self.assertEquals(m.title, 'Bastardi senza gloria')
        self.assertEquals(m.directorsLabel, 'Regista:')
        self.assertEquals(m.actorsLabel, 'Cast:')

    def testEs(self):
        m = imdbParser.IMDbParser('www', 'es', '0361748')
        self._checkGlobalData(m)
        self.assertEquals(m.title, 'Malditos bastardos')
        self.assertEquals(m.directorsLabel, 'Director:')
        self.assertEquals(m.actorsLabel, 'Reparto:')

class TestImdbParserTVShow(unittest.TestCase):

    def _checkGlobalData(self, m):
        self.assertEquals(m.year, '2005')
        self.assertTrue(m.isTvSerie)
        self.assertEquals(len(m.directors), 0)
        self.assertEquals(len(m.creators), 2)
        self.assertEquals(m.creators[0].name, 'Carter Bays')
        self.assertEquals(m.creators[0].url, '/name/nm0063215/')
        self.assertEquals(m.creators[1].name, 'Craig Thomas')
        self.assertEquals(m.creators[1].url, '/name/nm0858657/')
        self.assertEquals(len(m.actors), 6)
        self.assertEquals(m.actors[0].name, 'Josh Radnor')
        self.assertEquals(m.actors[0].url, '/name/nm1102140/')
        self.assertEquals(m.actors[1].name, 'Jason Segel')
        self.assertEquals(m.actors[1].url, '/name/nm0781981/')
        
    def testCom(self):
        m = imdbParser.IMDbParser('www', 'com', '0460649')
        self._checkGlobalData(m)
        self.assertEquals(m.title, '&#x22;How I Met Your Mother&#x22;')
        self.assertEquals(m.creatorsLabel, 'Creators:')
        self.assertEquals(m.actorsLabel, 'Cast:')
        
    def testUk(self):
        m = imdbParser.IMDbParser('uk', 'com', '0460649')
        self._checkGlobalData(m)
        self.assertEquals(m.title, '&#x22;How I Met Your Mother&#x22;')
        self.assertEquals(m.creatorsLabel, 'Creators:')
        self.assertEquals(m.actorsLabel, 'Cast:')

    def testFr(self):
        m = imdbParser.IMDbParser('www', 'fr', '0460649')
        self._checkGlobalData(m)
        self.assertEquals(m.title, '"How I Met Your Mother"')
        self.assertEquals(m.creatorsLabel, 'Cr&#xE9;ateurs:')
        self.assertEquals(m.actorsLabel, 'Ensemble:')

    def testDe(self):
        m = imdbParser.IMDbParser('www', 'de', '0460649')
        self._checkGlobalData(m)
        self.assertEquals(m.title, '"How I Met Your Mother"')
        self.assertEquals(m.creatorsLabel, 'Sch&#xF6;pfer:')
        self.assertEquals(m.actorsLabel, 'Besetzung:')

    def testIt(self):
        m = imdbParser.IMDbParser('www', 'it', '0460649')
        self._checkGlobalData(m)
        self.assertEquals(m.title, '"E alla fine arriva mamma!"')
        self.assertEquals(m.creatorsLabel, 'Creatori:')
        self.assertEquals(m.actorsLabel, 'Cast:')

    def testEs(self):
        m = imdbParser.IMDbParser('www', 'es', '0460649')
        self._checkGlobalData(m)
        self.assertEquals(m.title, '"C&#xF3;mo conoc&#xED; a vuestra madre"')
        self.assertEquals(m.creatorsLabel, 'Creadores:')
        self.assertEquals(m.actorsLabel, 'Reparto:')
                

if __name__ == '__main__':
    unittest.main()
