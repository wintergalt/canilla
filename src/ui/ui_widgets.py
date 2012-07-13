from PyQt4.QtCore import * #@UnusedWildImport
from PyQt4.QtGui import * #@UnusedWildImport
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%d %b %Y %H:%M:%S')

HTML_COLORS = ['Black',
     'BlueViolet',
     'Brown',
     'CornflowerBlue',
     'Crimson',
     'DarkGreen',
     'DarkOrange',
     'DarkTurquoise',
     'DeepPink',
     'MediumAquaMarine',
     'YellowGreen']

class ThreadListModel(QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        ''' datain: a list where each item is a row'''
        QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.listdata)
    
    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.listdata[index.row()])
        else:
            return QVariant()
        
    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row + count - 1)
        if self.listdata and len(self.listdata) > row and len(self.listdata) > (row + count):
            self.listdata = self.listdata[:row] + self.listdata[row + count:]
            self.endRemoveRows()
            return True
        return False
    
    def clear(self):
        self.removeRows(0, len(self.listdata))
        
    def insertRows(self, rows):
        ''' rows is a list that is to be appended 
        at the end of self.listdata '''
        self.listdata.extend(rows)
        
    
class ThreadTreeModel(QStandardItemModel):
    
    def find_row_by_message_id(self, message_id):
        no_of_rows = self.rowCount()
        for row in range(no_of_rows):
            it = self.item(row)
            art = it.article
            if art.message_id == message_id:
                return row
        return -1
        
    def insert_rows(self, stored_articles):
        for art in stored_articles:
            items = []
            it = QStandardItem()
            it.article = art
            it.setData(art.headers['Subject'], Qt.DisplayRole)
            it.setCheckable(False)
            items.append(it)
            
            it = QStandardItem()
            it.article = art
            it.setData(art.headers['From'], Qt.DisplayRole)
            items.append(it)
            
            it = QStandardItem()
            it.article = art
            it.setData(art.headers['Date'], Qt.DisplayRole)
            items.append(it)
            
            if art.headers['References']:
                last_ref = self.get_last_ref(art.headers['References'])
                parent_row = self.find_row_by_message_id(last_ref)
            
            if parent_row >= 0:
                logging.debug('setting child...')
                self.item(parent_row).setChild(self.item(parent_row).rowCount(), items[0])
                self.item(parent_row).setChild(self.item(parent_row).rowCount(), items[1])
                self.item(parent_row).setChild(self.item(parent_row).rowCount(), items[2])
            else:
                self.appendRow(items)
            
            
            
        
    def get_last_ref(self, refs):
        if not refs:
            last_ref = None
        else:
            last_ref = refs.split(' ')[-1]
        return last_ref
            
    
    def insert_root_row(self):
        pass
    
    def data(self, index, role=Qt.DisplayRole):
        current_article = self.itemFromIndex(index).article
        if not current_article.read and role == Qt.FontRole:
            font = QFont()
            font.setBold(True)
            return font
            
        return QStandardItemModel.data(self, index, role)
        
        
    

