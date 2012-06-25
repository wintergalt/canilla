from model.bo import *
from datetime import datetime
from elixir import *

if __name__ == '__main__':
    setup_all(True)
    # clear tables
    session.query(Message).delete()
    session.query(Newsgroup).delete()
    session.query(NewsServer).delete()
    
    defaultServer = NewsServer(name=u'Default', 
        hostname='news.gmane.org')
    newsgroupOne = Newsgroup(name=u'gmane.comp.python.general', 
                   newsserver=defaultServer) 
    newsgroupTwo = Newsgroup(name=u'gmane.comp.python.django.user', 
                   newsserver=defaultServer) 
    messageOne = Message(subject='Test 1',
                         body='Body test 1',
                         date_sent=datetime.now(),
                         newsgroups=newsgroupOne)
    messageTwo = Message(subject='Test 2',
                         body='Body test 2',
                         date_sent=datetime.now(),
                         newsgroups=newsgroupOne)
    messageThree = Message(subject='Test 3',
                         body='Body test 3',
                         date_sent=datetime.now(),
                         newsgroups=newsgroupTwo)
    messageFour = Message(subject='Test 4',
                         body='Body test 4',
                         date_sent=datetime.now(),
                         newsgroups=newsgroupTwo)
    session.commit()
