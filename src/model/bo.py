from elixir import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport

metadata.bind = 'sqlite:///canilla.sqlite3'
metadata.bind.echo = True

class Message(Entity):
    using_options(tablename='messages')
    primary_key=True
    subject = Field(Unicode(255))
    body = Field(UnicodeText) 
    date_sent = Field(DateTime)
    newsgoups = ManyToMany('Newsgroup')
    
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
    