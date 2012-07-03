from bo import Preferences, Newsgroup, Message #@UnusedImport
from elixir import * #@UnusedWildImport
from sqlalchemy import desc
import logging #@UnusedImport
from nntp_stuff import * #@UnusedWildImport

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
    
    def retrieve_stored_messages(self, ng):
        return ng.messages
    
    def get_last_stored_message(self, ng):
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
        
    def get_stored_newsgroups(self, ns):
        if not ns:
            ns = self.get_default_server()
        return self.sql_session.query(Newsgroup).filter_by(newsserver=ns).all()
    
    def update_newsgroups(self):
        logging.fatal('Inside update_newsgroups')
        groups_to_add = []
        nntp_newsgroups = self.nntp.retrieve_newsgroups()
        stored_newsgroups = self.get_stored_newsgroups(self.default_server)
        logging.fatal('got stored_newsgroups: ')
        for ng in stored_newsgroups:
            logging.fatal(ng)
        stored_dict = dict(zip([ng.name for ng in stored_newsgroups], stored_newsgroups))
        groups_to_add = []
        for name, flag in nntp_newsgroups:
            if name not in stored_dict:
                groups_to_add.append(Newsgroup(name=name, flag=flag, subscribed=False, newsserver=self.default_server))
        
        self.sql_session.add_all(groups_to_add)
        self.sql_session.commit()
        
        