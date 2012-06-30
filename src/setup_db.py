from datetime import datetime
from model.bo import *
from elixir import * #@UnusedWildImport
import sys, os, logging

dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
dbfile = os.path.join(dbdir, 'canilla.sqlite3')

def init_db():
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    metadata.bind = 'sqlite:///%s' % dbfile
    metadata.bind.echo = True
    setup_all()
    if not os.path.exists(dbfile):
        create_all()
        session.query(Message).delete()
        session.query(Newsgroup).delete()
        session.query(NewsServer).delete()
        session.query(Preferences).delete()
        
        defaultServer = NewsServer(name=u'Default', 
            hostname='news.gmane.org',
            port=119)
        newsgroupOne = Newsgroup(name=u'gmane.comp.python.general', 
                       newsserver=defaultServer,
                       subscribed=True) 
        newsgroupTwo = Newsgroup(name=u'gmane.comp.python.django.user', 
                       newsserver=defaultServer,
                       subscribed=True) 
        messageOne = Message(subject='Test 1',
                             body='Body test 1',
                             date_sent=datetime.now(),
                             newsgroups=[newsgroupOne])
        messageTwo = Message(subject='Test 2',
                             body='Body test 2',
                             date_sent=datetime.now(),
                             newsgroups=[newsgroupOne])
        messageThree = Message(subject='Test 3',
                             body='Body test 3',
                             date_sent=datetime.now(),
                             newsgroups=[newsgroupTwo])
        messageFour = Message(subject='Test 4',
                             body='Body test 4',
                             date_sent=datetime.now(),
                             newsgroups=[newsgroupTwo])
        
        prefs = Preferences(default_server=defaultServer)
        
        session.commit()



if __name__ == '__main__':
    init_db()