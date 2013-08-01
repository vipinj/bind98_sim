#!/usr/bin/python

""" To make things simple'r, we create a resolver class
which runs a for loop to generate client requests. Basically, we first
make a request, choose a NS from the dict and then make a thread which 
waits for response from auth server """

import time
import threading
import Queue
from collections import deque


class Client(threading.Thread):
    def __init__(self, auth):
        super(Client, self).__init__()
        self.auth = auth

    def run(self):
        sleep_time = 50 + int(auth)*10
        time.sleep(sleep_time)
        return sleep_time

class Auth(object):
    def __init__(self):
        pass
        # nothing interesting here
        # self.tdict = {}
        # for i in range(13):
        #     self.tdict = []
        #     self.tdict[i].append(50 + i*10)
    def recv(self, num):
        sleep_time = (50 + num*10) * 0.001
        time.sleep(sleep_time)
        return sleep_time

class Resolver(object):

    def __init__(self, auth):
        self.rtt_d = {}
        self.resv_l = [threading.RLock() for i in range(13)]
        for i in range(13):
            self.rtt_d[i] = deque()
            self.rtt_d[i].append(50 + i*10)

    def run(self, cli_id):
        print 'req recd from client ', cli_id

        # with self.resv_l:
        rtt_l = []
        for i in range(0,13):
            tmp = self.rtt_d[i].pop()
            rtt_l.append(tmp)
            self.rtt_d[i].append(tmp)
        ns = rtt_l.index(min(rtt_l))
        for i in range(13):
            if i == ns:
                continue
            else:
                tmp2 = self.rtt_d[i].pop()
                rtt_d[i].append(tmp2*0.98)

        ret = self.auth(ns)
        with self.resv_l:
            val = self.rtt_d[ns][len(self.rtt_d[i])-1]
            self.rtt_d.append(0.7 * val + 0.3 * ret)
        print 'req done from client ', cli_id

    def start(self):
        thr_q = Queue.Queue()
        for i in range(1000):
            req = i # made a request, choose a ns
            rtt_l = []
            for j in range(13):
                tmp = self.rtt_d[j].pop()
                with self.resv_l[j]:
                    self.rtt_d[j].append(tmp)
                rtt_l.append(tmp)
            ns = rtt_l.index(min(rtt_l))
            thr_q.put(Client(ns))
        [i.run() for i in thr_q]
        [i.join() for i in thr_q]


def main():
    
    auth = Auth()
    resv = Resolver(auth)

    resv.start()

if __name__ == '__main__':
    main()
