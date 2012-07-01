from bo import Preferences, Newsgroup, Message
from elixir import * #@UnusedWildImport
import logging

class CanillaUtils():
    
    def __init__(self, sql_session):
        self.default_server = None
        self.sql_session = sql_session
        
    def get_default_server(self):
        prefs = self.sql_session.query(Preferences).first()
        return prefs.default_server
        
    def get_subscribed_groups(self, ns):
        logging.fatal('Inside get_subscribed_newsgroups')
        if not ns:
            ns = self.get_default_server()
        return self.sql_session.query(Newsgroup).filter_by(newsserver=ns).filter_by(subscribed=True).all()
    
    def retrieve_stored_messages(self, ng):
        logging.fatal('Inside retrieve_stored_headers')
        return ng.messages
    
