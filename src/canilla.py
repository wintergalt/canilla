from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from model.bo import Message, Newsgroup, NewsServer
from ui.main import Ui_MainWindow
from elixir import * #@UnusedWildImport
import sys, os, logging
from datetime import datetime
from nntplib import * #@UnusedWildImport
from ui.ui_widgets import * #@UnusedWildImport

dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
dbfile = os.path.join(dbdir, 'canilla.sqlite3')
nntp_conn = None


class MainWindow(QMainWindow):

    def ui_extra_setup(self):
        splitter_2 = self.mainwindow.splitter_2
        splitter_2.setSizes([30,200])    
        
        tv = self.mainwindow.tv_groups
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Newsgroups'])
        tv.setModel(model)
        tv.selectionModel().currentChanged.connect(self.group_selection_changed)
        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
        tv.setIndentation(0)
        
        lv = self.mainwindow.lv_headers
        listModel = ThreadListModel(datain=[])
        lv.setModel(listModel)
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainwindow = Ui_MainWindow()
        self.mainwindow.setupUi(self)
        self.ui_extra_setup()
        self.load_groups()
        
        
    def populate_threads(self, current):
        logging.debug('Inside populate_threads')
        lv = self.mainwindow.lv_headers
        lv.model().clear()
        logging.debug('lv headers cleared')
        currentItem = self.mainwindow.tv_groups.model().itemFromIndex(self.mainwindow.tv_groups.currentIndex())
        (reply, count, first, last, name) = nntp_conn.group(currentItem.newsgroup.name)
        lv.model().setdata
    
    
    def group_selection_changed(self, current, previous):
        logging.debug('Inside group_selection_changed')
        self.populate_threads(current)
    
    
    def load_groups(self):
        groups = session.query(Newsgroup).filter_by(subscribed=True)
        tv = self.mainwindow.tv_groups
        
        for g in groups:
            items = []
            logging.debug('Inside loop')
            it = QStandardItem()
            it.newsgroup = g
            it.setData(g.name, Qt.DisplayRole)
            it.setCheckable(False)
            items.append(it)
            tv.model().appendRow(items)
        
        tv.selectionModel().select(tv.model().index(0, 0), QItemSelectionModel.Select)
        currentGroup = tv.model().itemFromIndex(tv.currentIndex()) 
        logging.debug(currentGroup)

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
        
        defaultServer = NewsServer(name=u'Default', 
            hostname='news.gmane.org')
        newsgroupOne = Newsgroup(name=u'gmane.comp.python.general', 
                       newsserver=defaultServer,
                       subscribed=True) 
        newsgroupTwo = Newsgroup(name=u'gmane.comp.python.django.user', 
                       newsserver=defaultServer,
                       subscribed=True) 
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


def init_app():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S')
    global nntp_conn
    nntp_conn = NNTP('news.gmane.org', 119)


if __name__ == '__main__':
    init_db()
    init_app()
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()