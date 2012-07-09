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
    
    
    def calculate_first_to_retrieve(self, last_stored, last_in_server, max_headers):
        if (last_in_server - last_stored) > max_headers:
            first = last_in_server - max_headers
        else:
            first = last_stored + 1
        return first
    
    def retrieve_new_headers(self, newsgroup, last_stored, max_headers):
        (reply, count, first, last, name) = self.nntp_conn.group(newsgroup.name)
        
        headers_list = []
        first_to_retrieve = self.calculate_first_to_retrieve(last_stored, int(last), max_headers)
        (resp, list) = self.nntp_conn.xover(str(first_to_retrieve), last)
        for (article_number, subject, poster, date, id, references, size, lines) in list:
            d = {}
            d['Number'] = article_number
            d['Subject'] = subject
            d['From'] = poster
            d['Date'] = date
            d['Message-ID'] = id
            d['References'] = ' '.join(references)
            d['Lines'] = lines
            d['Newsgroups'] = newsgroup.name
            headers_list.append(d)
        
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
    
    
        