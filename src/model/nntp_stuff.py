from nntplib import *
import logging
from model.utils import CanillaUtils

class CanillaNNTP():
    
    def __init__(self, server, port=119):
        logging.fatal('server: %s' % server)
        logging.fatal('port: %d' % port)
        self.nntp_conn = NNTP(server.hostname, port)
        self.cu = CanillaUtils()
    
    def update_newsgroup(self, newsgroup):
        logging.fatal('updating newsgroups')
        pass
    
    def retrieve_new_headers(self, newsgroup):
        logging.fatal('retrieving headers')
        last_stored = self.cu.get_last_stored_message(newsgroup)
        (reply, count, first, last, name) = self.nntp_conn.group(newsgroup)
        (reply, subjects) = self.nntp_conn.xhdr('subject', str(int(last)-5) + '-' + last)
        headers = []
        for id, subject in subjects:
            d = {}
            try:
                reply, num, tid, list = self.nntp_conn.head(id)
            except NNTPTemporaryError:
                continue
            
            for line in list:
                for header in self.header_list:
                    header = line[:len(header)]
                    d[header] = line[len(header) + 2:]
                        
            headers.append(d)
        return headers
    
    def close_connection(self):
        logging.fatal('closing connection')
        self.nntp_conn.quit()