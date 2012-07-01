import unittest, os
from elixir import * #@UnusedWildImport
from model.utils import * #@UnusedWildImport
from model.bo import * #@UnusedWildImport

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
        
    def test_stored_messages(self):
        logging.info('testing get_stored_messages')
        ds = self.cu.get_default_server()
        subscribed_groups = self.cu.get_subscribed_groups(ds)
        self.assertIsNotNone(subscribed_groups)
        self.assertTrue(len(subscribed_groups) > 0)
        logging.info('len(subscribed_groups): %d' % len(subscribed_groups))
        for ng in subscribed_groups:
            self.assertIsInstance(ng, Newsgroup)
        first_newsgroup = subscribed_groups[0]
        self.assertIsNotNone(first_newsgroup)
        logging.info('first_newsgroup: %s' % first_newsgroup.name)
        
        stored_messages = self.cu.retrieve_stored_messages(first_newsgroup)
        self.assertIsNotNone(stored_messages)
        self.assertTrue(len(stored_messages) > 0)
        logging.info('len(stored_messages): %d' % len(stored_messages))
        for msg in stored_messages:
            self.assertIsInstance(msg, Message)
        