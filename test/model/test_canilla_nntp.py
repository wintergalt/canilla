import unittest
from elixir import * #@UnusedWildImport
from model.utils import * #@UnusedWildImport
from model.bo import * #@UnusedWildImport
from model.nntp_stuff import * #@UnusedWildImport
from setup_db import * #@UnusedWildImport

class TestCanillaNntp(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%d %b %Y %H:%M:%S')
        init_db()
        self.cu = CanillaUtils()
        self.current_newsserver = self.cu.get_default_server()
        self.nntp = CanillaNNTP(self.current_newsserver)
        
    
    def test_retrieve_newsgroups(self):
        logging.info('testing retrieve_newsgroups')
        ngs = self.nntp.retrieve_newsgroups()
        for idx, ng in enumerate(ngs):
            logging.fatal('ng: %s (%d)' % (ng, idx))
    