from __future__ import with_statement
from bo import Preferences, Newsgroup, Article #@UnusedImport
from elixir import * #@UnusedWildImport
from sqlalchemy import desc
import logging #@UnusedImport
from nntp_stuff import * #@UnusedWildImport
import time

class CanillaUtils():
    
    def __init__(self, nntp=None):
        self.default_server = None
        self.sql_session = session
        self.nntp = nntp
        
    def get_default_server(self):
        prefs = self.sql_session.query(Preferences).first()
        return prefs.default_server
        
    def get_subscribed_groups(self, ns):
        if not ns:
            ns = self.get_default_server()
        return self.sql_session.query(Newsgroup).filter_by(newsserver=ns).filter_by(subscribed=True).all()
    
    def retrieve_stored_articles(self, ng):
        return ng.articles
    
    def get_last_stored_article(self, ng):
        return self.sql_session.query(Article)\
            .filter(Article.newsgroups.comparator.contains(ng))\
            .order_by(desc(Article.number)).first()
            
    def get_max_headers(self):
        return self.sql_session.query(Preferences.max_headers).first()[0]
    
    def store_new_headers(self, headers_list):
        timer = Timer()
        with timer:
            for d in headers_list:
                article_newsgroups = []
                article = Article(message_id=d['Message-ID'], number=d['Number'], headers=d, read=False)
                ns_list = d['Newsgroups'].split(',')
                for ns in ns_list:
                    stored_newsgroup = self.sql_session.query(Newsgroup).filter_by(name=ns).first()
                    if stored_newsgroup:
                        article_newsgroups.append(stored_newsgroup)
                article.newsgroups = article_newsgroups
            self.sql_session.commit()
        logging.fatal('duration of store_new_headers: %d' % timer.duration_in_seconds())
        
    def get_stored_newsgroups(self, ns):
        if not ns:
            ns = self.get_default_server()
        return self.sql_session.query(Newsgroup).filter_by(newsserver=ns).all()
    
    def update_newsgroups(self):
        nntp_newsgroups = self.nntp.retrieve_newsgroups()
        stored_newsgroups = self.get_stored_newsgroups(self.default_server)
        stored_dict = dict(zip([ng.name for ng in stored_newsgroups], stored_newsgroups))
        groups_to_add = []
        for name, flag in nntp_newsgroups:
            if name not in stored_dict:
                groups_to_add.append(Newsgroup(name=name, flag=flag, subscribed=False, newsserver=self.get_default_server()))
        
        self.sql_session.add_all(groups_to_add)
        self.sql_session.commit()
        
    def mark_article_read(self, article):
        article.read = True
        self.sql_session.commit()
        
class Timer(object):
    
    def __enter__(self):
        self.__start = time.time()
    
    def __exit__(self, type, value, traceback):
        self.__finish = time.time()
        
    def duration_in_seconds(self):
        return self.__finish - self.__start
    
    
        