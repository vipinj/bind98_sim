#!/usr/bin/python

import logging
import time
import copy_reg, copy, pickle
import threading
from multiprocessing import Pool, Array, Manager
import types

lgr = logging.getLogger('resolver')
lgr.setLevel(logging.DEBUG)
fh = logging.FileHandler('bind.log')
fh.setLevel(logging.DEBUG)
frmt = logging.Formatter('%(asctime)s, %(message)s')
fh.setFormatter(frmt)
lgr.addHandler(fh)

g_l = threading.Rlock()
g_rttd = {}
for j in range(13):
    g_rttd[j] = []
    g_rttd[j].append(50 + j*10)

# class AuthServer(object):
#     ''' Auth replies back to resolver, each server gets 50 +i*10 msec 
#     latency, where i = [1,13] '''
#     def __init__(self):
#         self.ns_dict = {}
#         for i in range(0,13):
#             self.ns_dict[i] = 50 + i*10
#     def auth(self, ns): 
#         sleep_time =  int(self.ns_dict[ns])
#         print 'sleeping  for time ', sleep_time
#         return sleep_time

def resolver(i):
    Tmin_l = []
    with g_l:
        for i,j in g_rttd.iteritems():
            Tmin_l.append(g_rttd[i][len(g_rttd[i])-1])
    Tmin = Tmin_l.index(min(Tmin_l))
    sleep_time = 50 + Tmin*10
    time.sleep(sleep_time)
    with g_l:
        g_rttd[Tmin].append(sleep_time)
        
    lgr.debug('Query from %d slept for time %f' %(i, sleep_time))
    return

class Server(object):
''' resolver server '''
    def __init__(self, port):
        self.port = port
        self.lgr = logging.getLogger('resolver')
        
    def run(self):
        print 'init server'
        s = socket.socket()
        a = tuple()
        a = (localhost, self.port)
        s.bind(a)
        s.listen(100)
        While True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            lgr.debug('got query from %d' %data)
            resolver(data)
            
        sys.exit()


if __name__ == '__main__':
    main()
