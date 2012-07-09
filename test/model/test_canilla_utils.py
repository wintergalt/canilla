import unittest, os
from elixir import * #@UnusedWildImport
from model.utils import * #@UnusedWildImport
from model.bo import * #@UnusedWildImport
from setup_db import *

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
        init_db()
        self.cu = CanillaUtils()
        nntp = CanillaNNTP(self.cu.get_default_server())
        self.cu.nntp = nntp
        self.cu.default_server = self.cu.get_default_server()
        
        
    def test_default_server(self):
        logging.info('testing get_default_server')
        ds = self.cu.get_default_server()
        self.assertIsInstance(ds, NewsServer)
        self.assertEqual('news.gmane.org', ds.hostname)
        
        
    def test_subscribed_groups(self):
        logging.info('testing get_subscribed_groups')
        default_newsserver = self.cu.get_default_server()
        subscribed_groups = self.cu.get_subscribed_groups(default_newsserver)
        assert len(subscribed_groups) > 0
        for ng in subscribed_groups:
            self.assertIsInstance(ng, Newsgroup)
        
        
    def test_stored_articles(self):
        logging.info('testing get_stored_articles')
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
        
        stored_articles = self.cu.retrieve_stored_articles(first_newsgroup)
        self.assertIsNotNone(stored_articles)
        self.assertTrue(len(stored_articles) > 0)
        logging.info('len(stored_articles): %d' % len(stored_articles))
        for msg in stored_articles:
            self.assertIsInstance(msg, Article)
        
        
    def test_max_article_number(self):
        logging.info('testing get_max_article_number')
        ds = self.cu.get_default_server()
        first_group = self.cu.get_subscribed_groups(ds)[0]
        logging.info('group id is %d' % first_group.id)
        last_article = self.cu.get_last_stored_article(first_group)
        self.assertIsNotNone(last_article)
        self.assertIsInstance(last_article, Article)
        logging.info('last article number: %d' % last_article.number)
        
        
    def test_update_newsgroups(self):
        logging.info('testing update_newsgroups')
        self.cu.update_newsgroups()