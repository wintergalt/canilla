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
    
    def data(self, index, role=Qt.DisplayRole):
        currentMessage = self.itemFromIndex(index).message
        #logging.debug('---- inside data for message_id %s and read is %s, while role is %s' % (currentMessage.message_id, currentMessage.read, role))
        if not currentMessage.read and role == Qt.FontRole:
            font = QFont()
            font.setBold(True)
            return font
            
        return QStandardItemModel.data(self, index, role)
        
        
    

