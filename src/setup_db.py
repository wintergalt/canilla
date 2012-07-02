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
        '''
        messageOne = Message(read=False,
                             message_id='messageOne',
                             number=1,
                             headers = {'Subject':'Message One', 'From':'diego1@python.org', 'Date':'Mon, 2 Jul 2012 08:28:24 -0700 (PDT)'},
                             newsgroups=[newsgroupOne])
        messageTwo = Message(read=False,
                             message_id='messageTwo',
                             number=2,
                             headers = {'Subject':'Message Two', 'From':'diego2@python.org', 'Date':'Mon, 2 Jul 2012 09:28:24 -0700 (PDT)'},
                             newsgroups=[newsgroupOne])
        messageOne = Message(read=False,
                             message_id='messageThree',
                             number=3,
                             headers = {'Subject':'Message Three', 'From':'diego3@python.org', 'Date':'Mon, 2 Jul 2012 10:28:24 -0700 (PDT)'},
                             newsgroups=[newsgroupTwo])
        messageOne = Message(read=False,
                             message_id='messageFour',
                             number=4,
                             headers = {'Subject':'Message Four', 'From':'diego4@python.org', 'Date':'Mon, 2 Jul 2012 11:28:24 -0700 (PDT)'},
                             newsgroups=[newsgroupTwo])
                             '''
        
        prefs = Preferences(default_server=defaultServer, max_headers=5)
        
        
        session.commit()



if __name__ == '__main__':
    init_db()