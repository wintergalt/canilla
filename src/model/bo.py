from elixir import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
import os

dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
dbfile = os.path.join(dbdir, 'canilla.sqlite3')
metadata.bind = 'sqlite:///%s' % dbfile
metadata.bind.echo = True
    
class Message(Entity):
    using_options(tablename='messages')
    primary_key=True
    subject = Field(Unicode(255))
    date_sent = Field(DateTime)
    newsgroups = ManyToMany('Newsgroup')
    read = Field(Boolean)
    message_id = Field(Unicode(255))
    number = Field(Integer)
    
    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)
        self.body = ''
    
    def __repr__(self):
        return self.subject

class Newsgroup(Entity):
    using_options(tablename='newsgroups')
    primary_key=True
    name = Field(Unicode(255))
    subscribed = Field(Boolean)
    messages = ManyToMany('Message')
    newsserver = ManyToOne('NewsServer')
    
    def abbreviated_name(self):
        l = self.name.split('.')
        return '.'.join([n[0] for n in l])
        
    def __repr__(self):
        return self.name
    
class NewsServer(Entity):
    using_options(tablename='newsservers')
    primary_key=True
    name = Field(Unicode(255))
    hostname = Field(Unicode(255))
    port = Field(Integer, default=119)
    newsgroups = OneToMany('Newsgroup')
    prefs = ManyToOne('Preferences')
    
    def __repr__(self):
        return self.name
    
class Preferences(Entity):
    using_options(tablename='preferences')
    primary_key = True
    default_server = OneToOne('NewsServer', inverse='prefs')