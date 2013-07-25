#!/usr/bin/python

import time
import logging
import random
import Queue
import threading

rtt_dict = {}
for i in range(0,13):
    rtt_dict[i] = []
    rtt_dict[i].append(50 + i*10)


class Client(threading.Thread):
    def __init__(self, resv):
        super(Client, self).__init__()
        self.resv = resv

    def run(self):
        t = random.randint(1,10000)
        if t == self.resv.run(t):
            return

class AuthServer(object):
    ''' Auth replies back to resolver, each server gets 50 +i*10 msec 
    latency, where i = [1,13] '''
    def __init__(self):
        self.ns_dict = {}
        for i in range(0,13):
            self.ns_dict[i] =  50 + i*10
    def auth(self, ns): 
        sleep_time =  self.ns_dict[ns]
        time.sleep(sleep_time * 0.001)
        return sleep_time

class Resolver(object):
    ''' client + resolver, generates queries and records rtts'''
    def __init__(self, auth):
        self.lgr = logging.getLogger('resolver')
        self.auths = auth
        self.rtt_l = threading.RLock()
        self.rtt_list = []
        with self.rtt_l:
            for i in range(0,13): # init with same rtts
                self.rtt_list.insert(i, (50 + i*10))

    def run(self, i):
        lgr = logging.getLogger('resolver')
        with self.rtt_l:
            # ns = self.rtt_list.index(min(self.rtt_list))
            tmp = min(self.rtt_list)
            ns = self.rtt_list.index(tmp)
            t_l = [str(i) for i in self.rtt_list]
            t_l2 = ','.join(t_l)
            lgr.debug('query sent to %d with %s' %(ns, t_l2))
            for j in range(13):
                if j == ns:
                    continue
                else:
                    self.rtt_list[j] = self.rtt_list[j] * 0.98

        ret = self.auths.auth(ns)
        lgr.debug('query %d returned with rtt %s' %(i, ret))
        with self.rtt_l:
            # print time.time() - t
            tmp = self.rtt_list[ns] 
            self.rtt_list[ns] = ret
            #(tmp * 0.70 + ret * 0.30)
        return i

def main():

    lgr = logging.getLogger('resolver')
    lgr.setLevel(logging.DEBUG)
    fh = logging.FileHandler('bind.log')
    fh.setLevel(logging.DEBUG)
    frmt = logging.Formatter('%(relativeCreated)d, %(message)s')
    fh.setFormatter(frmt)
    lgr.addHandler(fh)

    auth = AuthServer()
    resv = Resolver(auth)

    for j in range(1,100):
        l = []
        for i in range(1000):
            l.append(Client(resv))

        [i.start() for i in l]
        [i.join() for i in l]

if __name__ == '__main__':
    main()    
