from elixir import * #@UnusedWildImport
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy
from PyQt4.QtGui import * #@UnusedWildImport
import os

dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
dbfile = os.path.join(dbdir, 'canilla.sqlite3')
metadata.bind = 'sqlite:///%s' % dbfile
metadata.bind.echo = False
    
class Header(Entity):
    using_options(tablename='headers')
    primary_key=True
    header_name = Field(Unicode(500))
    header_value = Field(Unicode(500))
    article = ManyToOne('Article')
    
    #see http://docs.sqlalchemy.org/en/rel_0_7/orm/collections.html#custom-dictionary-based-collections
    
    def __init__(self, hn, hv):
        self.header_name = hn
        self.header_value = hv
        
    def __repr__(self):
        return '[', self.header_name, ':', self.header_value, ']'

class Article(Entity):
    using_options(tablename='articles')
    primary_key=True
    newsgroups = ManyToMany('Newsgroup')
    read = Field(Boolean)
    message_id = Field(Unicode(255))
    number = Field(Integer)
    headersdict = OneToMany('Header', collection_class=attribute_mapped_collection('header_name'))
    headers = association_proxy('headersdict', 'header_value', creator=Header)
    
    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)
        # body is a transient attribute
        self.body = ''
    
    def __repr__(self):
        return '[message number: %d]' % self.number
    
class Newsgroup(Entity):
    using_options(tablename='newsgroups')
    primary_key=True
    name = Field(Unicode(255), unique=True)
    subscribed = Field(Boolean)
    flag = Field(Unicode(1))
    articles = ManyToMany('Article')
    newsserver = ManyToOne('NewsServer')
    
    def abbreviated_name(self):
        l = self.name.split('.')
        return '.'.join([n[0] for n in l])
        
    def __repr__(self):
        return self.name
    
class NewsServer(Entity):
    using_options(tablename='newsservers')
    primary_key=True
    name = Field(Unicode(255), unique=True)
    hostname = Field(Unicode(255), unique=True)
    port = Field(Integer, default=119)
    newsgroups = OneToMany('Newsgroup')
    prefs = ManyToOne('Preferences')
    
    def __repr__(self):
        return self.name
    
class Preferences(Entity):
    using_options(tablename='preferences')
    primary_key = True
    default_server = OneToOne('NewsServer', inverse="prefs")
    max_headers = Field(Integer)
    
    def __repr__(self):
        return '[default_server: %s]' % self.default_server
    
    