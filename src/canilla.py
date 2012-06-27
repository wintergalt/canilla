from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from model.bo import Message, Newsgroup, NewsServer
from ui.main import Ui_MainWindow
from elixir import * #@UnusedWildImport
import sys, os, logging
from datetime import datetime
from nntplib import * #@UnusedWildImport
from ui.ui_widgets import * #@UnusedWildImport
from ui import ui_widgets

dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
dbfile = os.path.join(dbdir, 'canilla.sqlite3')
nntp_conn = None


class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainwindow = Ui_MainWindow()
        self.mainwindow.setupUi(self)
        self.header_list = ['Subject', 'From', 'Date']
        self.ui_extra_setup()
        self.load_groups()
        
        
    def ui_extra_setup(self):
        splitter_2 = self.mainwindow.splitter_2
        splitter_2.setSizes([30,200])    
        
        tv_groups = self.mainwindow.tv_groups
        groups_model = QStandardItemModel()
        groups_model.setHorizontalHeaderLabels(['Newsgroups'])
        tv_groups.setModel(groups_model)
        tv_groups.selectionModel().currentChanged.connect(self.group_selection_changed)
        tv_groups.setSelectionBehavior(QAbstractItemView.SelectRows)
        tv_groups.setIndentation(0)
        
        tv_headers = self.mainwindow.tv_headers
        headers_model = QStandardItemModel()
        headers_model.setHorizontalHeaderLabels(self.header_list)
        tv_headers.setModel(headers_model)
        tv_headers.selectionModel().currentChanged.connect(self.header_selection_changed)
        tv_headers.setSelectionBehavior(QAbstractItemView.SelectRows)
        tv_headers.setIndentation(0)
        
        tb = self.mainwindow.tb_body
        tb.setLineWrapColumnOrWidth(76)
        tb.setLineWrapMode(QTextEdit.FixedColumnWidth)
        
    def show_next_article(self):
        logging.debug('show_next_article')
        
        
    def clear_headers_table(self):
        tv_headers = self.mainwindow.tv_headers
        tv_headers.model().clear()
        tv_headers.model().setHorizontalHeaderLabels(self.header_list)
    
    
    def populate_threads(self, current):
        tv_headers = self.mainwindow.tv_headers
        self.clear_headers_table()
        currentItem = self.mainwindow.tv_groups.model().itemFromIndex(self.mainwindow.tv_groups.currentIndex())
        (reply, count, first, last, name) = nntp_conn.group(currentItem.newsgroup.name)
        
        (reply, subjects) = nntp_conn.xhdr('subject', str(int(last)-5) + '-' + last)
        
        for id, subject in subjects:
            d = {}
            try:
                reply, num, tid, list = nntp_conn.head(id)
            except NNTPTemporaryError:
                continue
                
            for line in list:
                for header in self.header_list:
                    if line[:len(header)] == header:
                        d[header] = line[len(header) + 2:]
            
            items = []
            it = QStandardItem()
            it.id = id
            it.setData(d['Subject'], Qt.DisplayRole)
            it.setCheckable(False)
            items.append(it)
            
            it = QStandardItem()
            it.id = id
            it.setData(d['From'], Qt.DisplayRole)
            items.append(it)
            
            it = QStandardItem()
            it.id = id
            it.setData(d['Date'], Qt.DisplayRole)
            items.append(it)
            
            tv_headers.model().appendRow(items)
    
    
    def group_selection_changed(self, current, previous):
        self.populate_threads(current)
    
    
    def count_greater_thans(self, text):
        ''' Returns the number of leading '>'s in text '''
        if text:
            return len(text) - len(str.lstrip(text, '>'))
        else:
            return 0
    
    def format_text(self, lines):
        formatted_text = '<p>'
        for line in lines:
            level = self.count_greater_thans(line)
            formatted_text += '<font color="' + ui_widgets.HTML_COLORS[level] + '">' + line + '</font>' + '<br/>'
        formatted_text += '</p>'
        return formatted_text
        
    def populate_body(self, current):
        tb_body = self.mainwindow.tb_body
        tb_body.clear()
        tv_headers = self.mainwindow.tv_headers
        id = tv_headers.model().itemFromIndex(tv_headers.currentIndex()).id
        reply, num, tid, list = nntp_conn.body(id)
        body = self.format_text(list)
        tb_body.setText(body)
    
    def header_selection_changed(self, current, previous):
        self.populate_body(current)
        

    def load_groups(self):
        groups = session.query(Newsgroup).filter_by(subscribed=True)
        tv = self.mainwindow.tv_groups
        
        for g in groups:
            items = []
            it = QStandardItem()
            it.newsgroup = g
            it.setData(g.name, Qt.DisplayRole)
            it.setCheckable(False)
            items.append(it)
            tv.model().appendRow(items)
        
        tv.selectionModel().select(tv.model().index(0, 0), QItemSelectionModel.Select)
        #currentGroup = tv.model().itemFromIndex(tv.currentIndex()) 

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
    try:
        init_db()
        init_app()
        app = QApplication(sys.argv)
        frame = MainWindow()
        frame.show()
        app.exec_()
    finally:
        if nntp_conn:
            nntp_conn.quit()