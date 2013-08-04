#!/usr/bin/python
# argv[1] is the k factor for how often to run the monitor thread
# argv[2] is the k' factor for how much to wait for the response(k'*rtt)
import sys
import time
#import sched
import logging
#import random
#import Queue
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
        if self.cid == self.resv.run(self.cid, True):
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
        if ns == 7:
            pass
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
        self.queryl = threading.RLock()
        self.query_inprogress = {}
        self.tr_list = []
    def monitor(self):
        ''' monitor thread is responsible for monitoring timed out
        fx calls and do something about them '''
        self.lgr.debug('##### Monitor running #####')
        with self.statusl:
            if self.status:
                t = time.time()
                try:
                    for k,v in self.status.iteritems():
                        # packet has not returned, even after the RTT value
                        if v[len(v)-1] < t: 
                            # ns = v[0] # nameserver
                            self.lgr.debug('packet resent %s %s'
                                           %(k, ','.join([str(i) for i in v])))
                            #self.run(k, False) #runs into a recursion loop based on qids
                            t = threading.Thread(target=self.run, args = (k, False))
                            try:
                                t.start()
                                self.tr_list.append(t)
                            except:
                                l = []
                                l.append('Thread init error from monitor')
                                l.append(sys.argv[1])
                                l.append(sys.argv[2])
                                st = ' '.join(l)
                                print st
                                self.lgr.error('Thread init error from monitor ')
                                pass
                            continue
                            
                except RuntimeError, e: 
                    self.lgr.error('%s %s' %(e, sys.exc_info()))
                    # error for dictionary changing size, harmless by design.
                    pass

    def run(self, i, val):
        if i % int(sys.argv[1]) == 0 and val: 
            try:
                threading.Thread(target = self.monitor())
            except:
                er = []
                er.append('Thread init error from run')
                er.append(sys.argv[1])
                er.append(sys.argv[2])
                st = ' '.join(er)
                print st
                self.lgr.error('Thread init error from run')
                pass
                
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
                self.status[i].append(tstamp + int(sys.argv[2])*old_rtt)
            else:
                # print i
                self.status[i] = []
                self.status[i].append(tstamp + int(sys.argv[2])*old_rtt)
                
        lgr.debug('query %d sent to %d with %s' %(i, ns, t_l2))
             
        with self.queryl:
            self.query_inprogress[i] = threading.Thread.ident

        ret = self.auths.auth(ns, i)
        if not ret:
            # print 'OUT'
            time.sleep(2)
            with self.rtt_l:
                self.rtt_list[ns] = 2000 # for now, the max timeout val=2 sec
            with self.queryl:
                self.query_inprogress.pop(i, None)
            return i
        with self.queryl:
            self.query_inprogress.pop(i, None)

        lgr.debug('query %d returned with rtt %s' %(i, ret))

        with self.statusl:
            self.status.pop(i, None)
        with self.rtt_l:
            tmp = self.rtt_list[ns] 
            self.rtt_list[ns] = ret
            #(tmp * 0.70 + ret * 0.30)
        return i
    
    def __del__(self):
        [i.join() for i in self.tr_list]


def main():

    lgr = logging.getLogger('resolver')
    lgr.setLevel(logging.DEBUG)
    fname='bind.log_'+sys.argv[2]+'_'+sys.argv[1]
    fh = logging.FileHandler(fname)
    fh.setLevel(logging.DEBUG)
    frmt = logging.Formatter('%(relativeCreated)d, %(levelname)s, %(lineno)d, %(message)s')
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
    resv.__del__()

if __name__ == '__main__':
    main()    
