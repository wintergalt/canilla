from bo import Preferences, Newsgroup, Message
from elixir import * #@UnusedWildImport
from sqlalchemy import desc
import logging

class CanillaUtils():
    
    def __init__(self):
        self.default_server = None
        self.sql_session = session
        
    def get_default_server(self):
        prefs = self.sql_session.query(Preferences).first()
        return prefs.default_server
        
    def get_subscribed_groups(self, ns):
        logging.debug('Inside get_subscribed_newsgroups')
        if not ns:
            ns = self.get_default_server()
        return self.sql_session.query(Newsgroup).filter_by(newsserver=ns).filter_by(subscribed=True).all()
    
    def retrieve_stored_messages(self, ng):
        logging.debug('Inside retrieve_stored_headers')
        return ng.messages
    
    def get_last_stored_message(self, ng):
        logging.debug('Inside get_last_stored_message(%s)' % ng.name)
        return self.sql_session.query(Message)\
            .filter(Message.newsgroups.comparator.contains(ng))\
            .order_by(desc(Message.number)).first()
            
    def get_max_headers(self):
        return self.sql_session.query(Preferences.max_headers).first()[0]
    
    def store_new_headers(self, headers_list):
        
        for d in headers_list:
            message_newsgroups = []
            message = Message(message_id=d['Message-ID'], number=d['Number'], headers=d, read=False)
            ns_list = d['Newsgroups'].split(',')
            for ns in ns_list:
                stored_newsgroup = self.sql_session.query(Newsgroup).filter_by(name=ns).first()
                if stored_newsgroup:
                    message_newsgroups.append(stored_newsgroup)
            message.newsgroups = message_newsgroups
        self.sql_session.commit()
        
        
    
    
    
    
    