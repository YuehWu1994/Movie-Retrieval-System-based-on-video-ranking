#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import server

class LoadBalancingManager:
    def __init__(self, initServer):
        self.time = 0
        self.serverList = [server(20, 20, 20)] * initServer
        self.numberOfServer = initServer
        
        # create movieId to list of server mapping <int, vector<int>>
        self.movieIdTable = dict()
        
    #
        
    
    def updateLoad(self):
        hasLoad = False
        
        for i in self.numberOfServer:
            if(self.serverList.updateLoad() > 0):
                hasLoad = True
                
        return hasLoad
    
    def getNumberOfServer(self):
        return self.numberOfServer
    
    def getDuplicatedRate(self):
        cnt = 0
        for it in self.movieIdTable.values():
            cnt += it
        return cnt/self.movieIdTable.size()
    
    
    
    
    # every second, store/ update load from every server
    
    # server
        # declare cache list
        # which movies are in the cache
        # update cache list in specific time interval
    
    # LoadBalancingManager
        # init: distribute movies to servers (location and size of movie are randomly distributed)
        # algo: find most suitable server to execute the movie request
            # movie is in the server
            # movie store in cache or disk
            
        # declare cache table
        # udpate cache table

    # main: 
        # send movieRequest to loadbalancingManager
    
    # duplication
        # server crash
        # request >= threshold / load >= threshold
        
    # de-replicate
        # number of request in specific time interval 
        
    # cache access time
    # disk access time
    # request access time
        
            
        
        
        
        
