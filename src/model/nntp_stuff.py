from nntplib import *
import logging
from model.utils import CanillaUtils
import string

class CanillaNNTP():
    
    def __init__(self, server, port=119):
        logging.fatal('server: %s' % server)
        logging.fatal('port: %d' % port)
        self.server = server
        self.nntp_conn = NNTP(server.hostname, port)
        self.cu = CanillaUtils()
    
    def update_newsgroup(self, newsgroup):
        logging.fatal('updating newsgroups')
        pass
    
    def calculate_range(self, last_stored, last):
        if last_stored == last:
            return None
        max_headers_to_retrieve = self.cu.get_max_headers()
        if (last - last_stored) > max_headers_to_retrieve:
            min_range = last - max_headers_to_retrieve
        else:
            min_range = last_stored
        return str(min_range) + '-' + str(last)
        
    
    def retrieve_new_headers(self, newsgroup):
        last_stored = self.cu.get_last_stored_message(newsgroup)
        (reply, count, first, last, name) = self.nntp_conn.group(newsgroup.name)
        range = self.calculate_range(last_stored.number if last_stored else 0, int(last))
        
        if not range:
            return []
        
        (reply, subjects) = self.nntp_conn.xhdr('subject', range)
        headers_list = []
        for id, subject in subjects:
            d = {}
            try:
                reply, num, tid, list = self.nntp_conn.head(id)
                d['Number'] = num
            except NNTPTemporaryError:
                continue
                
            header_name = ''
            header_value = ''
            
            for line in list:
                if line[0] in string.whitespace:
                    # append new line to previous line
                    d[header_name] = d[header_name] + '\n' + line
                    continue
                idx = line.index(':')
                header_name = line[:idx]
                header_value = line[idx + 2:]
                d[header_name] = header_value
                        
            headers_list.append(d)
        
        return headers_list
    
    def retrieve_body(self, message_id):
        logging.fatal('type of id: %s' % type(message_id))
        logging.fatal('message_id: %s' % message_id)
        reply, num, tid, list = self.nntp_conn.body(message_id)
        logging.fatal('type of list: %s' % type(list))
        return list
        
    def retrieve_newsgroups(self):
        response, list = self.nntp_conn.list()
        logging.fatal('response: %s' % response)
        for line in list:
            group, hi, lo, flag = line
            
            now store this information in the db
            
            
        
    def close_connection(self):
        logging.fatal('closing connection')
        self.nntp_conn.quit()