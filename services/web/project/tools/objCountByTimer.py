'''
Class which populated quantity of hashcodes by time scale :  [1 minute, 5 minutes, ..., 60 minutes  ]
to get how many unique hashcode were populated call self.get(i) where i index of time scale
self.get(0): return how many hash codes populated for last minutes
self.get(1): return how many hash codes populated for last 5 minutes
...
self.get(n): return how many hash codes populated for last 60 minutes

self.add(hash): To add hash code to the queue
override or change self.equals(hash1, hash2) method

'''
from collections import deque

import threading
import time

class ObjCountByTimer:
    ''' This class count different objects ( by hashcode) by using timer  '''
    def __init__(self, timestep=1, timescope=85, time_scale=(1,5,60,80)):
        self.store = deque()
        self.timescope = timescope # in seconds
        self.timestep = timestep # in seconds
        self.interval = 0
        self.time_scale = time_scale
        self.counted = []
        for i in range(len(time_scale)): self.counted.append(0)
        self.t1 = threading.Timer(timestep, self.scheduler)
        self.t1.start()
      
    def right_shift(self, elem, index):
        #print("self.time_scale: {}".format(self.time_scale) )
        for _i in range(len(self.time_scale)):
            #print("t:{} ,elem:{}".format(self.time_scale[_i],elem))
            if self.time_scale[_i] >= elem[0]:
                #shift all elements on 1 sec to right
                self.counted[_i] = index + 1
                return
            else:
                self.counted[_i] = 0
                

    def scheduler(self):
        ''' This scheduler called by timer every self.timescope/10 sec '''
        #print("Scheduler called queue: {}".format(list(self.store)))
        ls = list(self.store)
        #print("ls[0]: {}".format(ls[0]) )
        #print("ls[0]: {} len(ls): {} ".format(ls[0], len(ls)) )
        #print("self.counted {}".format(self.counted))
        for index in range(len(ls)):
            #print("elem:{}".format(ls[index]))
            ls[index][0] += self.timestep # increase in seconds
            #slice 
            self.right_shift(ls[index], index)
            # when we reach last second of timescope
            if ls[index][0] > self.timescope: 
                #remove the last element from the queue  which is out of time scope
                del self.store[index]
                break
        self.t2 = threading.Timer(self.timestep, self.scheduler)
        self.t2.start()
    def stop(self):
        self.t1.cancel()    
        self.t2.cancel()
        
    #implements equals override it in child class
    def equals(self,hash1, hash2):
        return hash1==hash2
        
    def getCountedObjects(self):
        return max(self.counted)    
    
    def toString(self, prefix = '', postfix= ''):
        ls = list(self.store)
        return [ prefix + str(val[1]) + postfix for val in ls] 
        
    def add(self,hashcode):
        ''' Add a new object to queue , only if there is no "equal" objects ''' 
        n=0
        for elem in list(self.store):
            if self.equals(hashcode, elem[1]):
                break
            n+=1
        #print('self.store.qsize({}), n={}'.format(len(self.store), n))    
        ret = len(self.store) == n
        if ret:
            self.store.append([0,hashcode])
        return  ret

