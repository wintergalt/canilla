from bo import Preferences, Newsgroup, Message
from elixir import *
import logging

class CanillaUtils():
    
    def __init__(self, sql_session):
        self.default_server = None
        self.sql_session = sql_session
        
    def get_default_server(self):
        #prefs = Preferences.query.first()
        prefs = self.sql_session.query(Preferences).first()
        return prefs.default_server
        
    def get_subscribed_groups(self, ns):
        logging.fatal('Inside get_subscribed_newsgroups')
        if not ns:
            ns = self.get_default_server()
        return self.sql_session.query(Newsgroup).filter_by(newsserver=ns).filter_by(subscribed=True).all()
    
    def retrieve_stored_headers(self, ng):
        logging.fatal('Inside retrieve_stored_headers')
        #messages = Message.query.filter_by(newsgroup=ng)
        messages = self.sql_session.query(Message).filter_by(newsgroup=ng).all()
        headers = []
        for m in messages:
            d = {}

            for line in list:
                for header in self.header_list:
                    if line[:len(header)] == header:
                        d[header] = line[len(header) + 2:]
                        
            headers.append(d)
        return headers
    
