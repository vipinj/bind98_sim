#!/usr/bin/python
"""
Pure simulation for bind 9.8 code-threaded version
The threads actually sleep, and return after their server's rtt
argv[1] is the k factor for how often to run the monitor thread
argv[2] is the k' factor for how much to wait for the response(k'*rtt)
"""

import sys
import time
import sched
import logging
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
        if ns == 7: # crashed server
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
        self.time_l = threading.RLock()
        self.time_torun = time.time()

    def run_monitor(self, t_val):
        if t_val > (self.time_torun + 0.075) and self.query_inprogress:
            try:
                t = threading.Thread(target = self.monitor())
                t.start()
                self.time_torun = time.time()
                return
            except:
                self.lgr.error('Thread init error from run')
                return
        else:
            return
        
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
                            t = threading.Thread(target=self.run, 
                                                 args = (k, False))
                            try:
                                t.start()
                                self.tr_list.append(t)
                            except:
                                self.lgr.error('Thread init error from monitor ')
                                pass
                            continue
                            
                except RuntimeError, e: 
                    """ Dictionary size changes as we remove answered queries, this is
                    harmless, and is by design """
                    self.lgr.error('%s %s' %(e, sys.exc_info()))
                    pass

    def run(self, i, val):
        with self.time_l:
            self.run_monitor(time.time())
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
                self.status[i].append(tstamp + int(sys.argv[1])*old_rtt)
            else:
                # print i
                self.status[i] = []
                self.status[i].append(tstamp + int(sys.argv[1])*old_rtt)
                
        lgr.debug('query %d sent to %d with %s' %(i, ns, t_l2))
             
        with self.queryl:
            self.query_inprogress[i] = threading.Thread.ident

        ret = self.auths.auth(ns, i)
        if not ret:
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
            #(tmp * 0.70 + ret * 0.30) # both fraction and non fraction
        return i
    
    def __del__(self):
        [i.join() for i in self.tr_list] # everyone is out before resolver exits

def main():

    lgr = logging.getLogger('resolver')
    lgr.setLevel(logging.DEBUG)
    fname='bind.log'+'_'+sys.argv[1]
    fh = logging.FileHandler(fname)
    fh.setLevel(logging.DEBUG)
    frmt = logging.Formatter('%(relativeCreated)d, %(levelname)s, %(lineno)d, %(message)s')
    fh.setFormatter(frmt)
    lgr.addHandler(fh)

    auth = AuthServer()
    resv = Resolver(auth)
    
    l = []
    for i in range(2000):
        cl = Client(resv, i)
        l.append(cl)
        cl.start()

    [i.join() for i in l]

    # sched design for timing events, not that great an idea
    # l_t1 = []
    # for i in range(2000):
    #     l_t1.append(Client(resv, i))
    # s = sched.scheduler(time.time, time.sleep)
    # s.enter(0, 1, run_thr, (l_t1, 999))
    # s.enter(0.5, 1, run_thr, (l_t1, 1001))
    # s.enter(0.9, 1, join_thr, (l_t1,))
    # s.run()

    resv.__del__()

if __name__ == '__main__':
    main()    
