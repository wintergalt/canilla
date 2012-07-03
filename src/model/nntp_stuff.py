from __future__ import with_statement
from nntplib import * #@UnusedWildImport
import logging
from model.bo import * #@UnusedWildImport
import string
import time

class CanillaNNTP():
    
    def __init__(self, server, port=119):
        logging.fatal('server: %s' % server)
        logging.fatal('port: %d' % port)
        self.server = server
        self.nntp_conn = NNTP(server.hostname, port)
    
    def update_newsgroup(self, newsgroup):
        logging.fatal('updating newsgroups')
        pass
    
    def calculate_range(self, last_stored, last, max_headers_to_retrieve):
        if last_stored == last:
            return None
        if (last - last_stored) > max_headers_to_retrieve:
            min_range = last - max_headers_to_retrieve
        else:
            min_range = last_stored
        return str(min_range) + '-' + str(last)
        
    
    def retrieve_new_headers(self, newsgroup, last_stored, max_headers):
        timer = Timer()
        with timer:
            (reply, count, first, last, name) = self.nntp_conn.group(newsgroup.name)
            range = self.calculate_range(last_stored.number if last_stored else 0, int(last), max_headers)
            
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
        
        logging.fatal('duration of retrieve_new_headers: %d' % timer.duration_in_seconds())
        
        return headers_list
    
    def retrieve_body(self, message_id):
        reply, num, tid, list = self.nntp_conn.body(message_id)
        return list
        
    def retrieve_newsgroups(self):
        timer = Timer()
        with timer:
            newsgroups = []
            response, list = self.nntp_conn.list()
            for line in list:
                group, hi, lo, flag = line
                newsgroups.append((group, flag))
        logging.fatal('duration of retrieve_newsgroups: %d' % timer.duration_in_seconds())
        return newsgroups
        
    def close_connection(self):
        logging.fatal('closing connection')
        self.nntp_conn.quit()
        
        
class Timer(object):
    
    def __enter__(self):
        self.__start = time.time()
    
    def __exit__(self, type, value, traceback):
        self.__finish = time.time()
        
    def duration_in_seconds(self):
        return self.__finish - self.__start
    
    
        