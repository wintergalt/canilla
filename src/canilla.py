from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
from model.bo import Message, Newsgroup, NewsServer, Preferences
from ui.main import Ui_MainWindow
from elixir import * #@UnusedWildImport
import sys, os, logging
from datetime import datetime
from nntplib import * #@UnusedWildImport
from ui.ui_widgets import * #@UnusedWildImport
from ui import ui_widgets
from model.nntp_stuff import CanillaNNTP
from model.utils import * 

dbdir = os.path.join(os.path.expanduser('~'), '.canilla')
dbfile = os.path.join(dbdir, 'canilla.sqlite3')

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mainwindow = Ui_MainWindow()
        self.mainwindow.setupUi(self)
        self.header_list = ['Subject', 'From', 'Date']
        self.ui_extra_setup()
        self.canilla_utils = CanillaUtils(session)
        self.current_newsserver = self.canilla_utils.get_default_server()
        self.nntp = CanillaNNTP(self.current_newsserver)
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
        # retrieve stored and new headers
        stored_headers = self.canilla_utils.retrieve_stored_headers(currentItem.newsgroup)
        new_headers = self.nntp.retrieve_headers(currentItem.newsgroup.name)
        # combine stored + new headers
        #now combine them!
        
        for d in new_headers:
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
        #groups = session.query(Newsgroup).filter_by(subscribed=True)
        groups = self.canilla_utils.get_subscribed_groups(self.current_newsserver)
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
        
    def closeEvent(self, *args, **kwargs):
        self.nntp.close_connection()
        return QMainWindow.closeEvent(self, *args, **kwargs)


def init_app():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S')


if __name__ == '__main__':
    init_app()
    app = QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()