#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import server
import random

class LoadBalancingManager:
    def __init__(self, numberOfServer, numberOfMovie, movieSizeLowerBound, movieSizeUpperBound):
        self.time = 0
        self.serverList = [server(20, 20, 20)] * numberOfServer
        self.numberOfServer = numberOfServer
        self.numberOfMovie = numberOfMovie
        
        # create movieId to list of server mapping <int, vector<int>>
        self.movieIdTable = dict()
        
        # distribute movies to servers (location and size of movie are randomly distributed)
        self.distributedMovie(movieSizeLowerBound, movieSizeUpperBound)
    
    def distributedMovie(self, movieSizeLowerBound, movieSizeUpperBound):
        for i in self.numberOfMovie:
            sv = random.randint(0, self.numberOfServer)
            self.serverList[sv].insertMovie(i, random.randint(movieSizeLowerBound, movieSizeUpperBound))
            
            # record in movieIdTable
            self.movieIdTable[i] = [sv] 
        
    
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
    
    
    ### TODO: distribute movies to servers ###
    def movieRequest(self, movieID, load):
        return False
    
    
    
    
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
        # send movieRequest to loadbalancingManager (number of movie, number of server)
    
    # duplication
        # server crash
        # request >= threshold / load >= threshold
        
    # de-replicate
        # number of request in specific time interval 
        
    # cache access time
    # disk access time
    # request access time
        
            
        
        
        
        
