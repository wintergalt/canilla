import unittest, os, logging
from elixir import *
from model.utils import *
from model.bo import *

class TestCanillaUtils(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%d %b %Y %H:%M:%S')
        dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
        dbfile = os.path.join(dbdir, 'canilla.sqlite3')
        metadata.bind = 'sqlite:///%s' % dbfile
        metadata.bind.echo = False
        setup_all()
        self.cu = CanillaUtils(session)
            
    def test_default_server(self):
        logging.info('testing get_default_server')
        ds = self.cu.get_default_server()
        self.assertIsInstance(ds, NewsServer)
        assert 'news.gmane.org' == ds.hostname
        
    def test_subscribed_groups(self):
        logging.info('testing get_subscribed_groups')
        default_newsserver = self.cu.get_default_server()
        subscribed_groups = self.cu.get_subscribed_groups(default_newsserver)
        assert len(subscribed_groups) > 0
        for ng in subscribed_groups:
            self.assertIsInstance(ng, Newsgroup)
        
        