#!/usr/bin/python

import sys
import time
import sched
import logging
import random
import Queue
import threading

rtt_dict = {}
for i in range(0,13):
    rtt_dict[i] = []
    rtt_dict[i].append(50 + i*10)


class Client(threading.Thread):
    def __init__(self, resv, i):
        super(Client, self).__init__()
        self.resv = resv
        self.cid = i

    def run(self):
        if self.cid == self.resv.run(self.cid):
            return

class AuthServer(object):
    ''' Auth replies back to resolver, each server gets 50 +i*10 msec 
    latency, where i = [1,13] '''
    def __init__(self):
        self.ns_dict = {}
        for i in range(0,13):
            self.ns_dict[i] =  50 + i*10
        self.lgr = logging.getLogger('resolver')

    def auth(self, ns, i): 
        sleep_time =  self.ns_dict[ns]
        #        if i%100 == 0:
        if ns == 7:
            sleep_time = sleep_time*0.001 + 2
            time.sleep(sleep_time)
            return sleep_time + 2000
        else:
            time.sleep(sleep_time*0.001)
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
        self.statusl = threading.RLock()
        self.status = {}

    def monitor(self):
        ''' monitor thread is responsible for monitoring timed out
        fx calls and do something about them '''
        self.lgr.debug('##### Monitor running #####')
        with self.statusl:
            while self.status:
                t = time.time()
                try:
                    for k,v in self.status.iteritems():
                        if v[len(v)-1] < t: # packet has not returned, even after the RTT value
                            self.lgr.debug('packet resent %s %s'
                                           %(k, ','.join([str(i) for i in v])))
                            self.run(k)
                except RuntimeError, e: 
                    self.lgr.error('%s' %e)
                    # error for dictionary changing size, harmless by design.
                    pass

    def run(self, i):
        if i == 1500 : 
            threading.Thread(target = self.monitor())
        lgr = logging.getLogger('resolver')
        with self.rtt_l:
            tmp = min(self.rtt_list)
            ns = self.rtt_list.index(tmp)
            t_l = [str(ii) for ii in self.rtt_list]
            t_l2 = ','.join(t_l)
            for j in range(13):
                if j == ns:
                    continue
                else:
                    self.rtt_list[j] = self.rtt_list[j] * 0.98

        # timeout infrastructure
        old_rtt = (50 + ns*10)*0.001 # 
        tstamp = time.time()
        with self.statusl:
            if i in self.status:
                self.status[i].append(tstamp + old_rtt)
            else:
                # print i
                self.status[i] = []
                self.status[i].append(tstamp + old_rtt)
                
        lgr.debug('query %d sent to %d with %s' %(i, ns, t_l2))
        st1 = '1,' + str(i)+','+ "{0:.5f}".format(time.time())
        print st1
        ret = self.auths.auth(ns, i)
        st2 = '2,' + str(i)+','+ "{0:.5f}".format(time.time())
        print st2
        lgr.debug('query %d returned with rtt %s' %(i, ret))

        with self.statusl:
            self.status.pop(i, None)
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

    for j in range(1,5):
        l = []
        for i in range(1000):
            l.append(Client(resv, i+j*1000))

        [i.start() for i in l]
        [i.join() for i in l]

if __name__ == '__main__':
    main()    
