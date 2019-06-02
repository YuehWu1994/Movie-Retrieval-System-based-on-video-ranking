#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from server import Server
import random
import sys

class LoadBalancingManager:
    def __init__(self, numberOfServer, numberOfMovie, movieSizeLowerBound, movieSizeUpperBound):
        self.serverList = [Server(20, 20, 20)] * numberOfServer
        self.numberOfServer = numberOfServer
        self.numberOfMovie = numberOfMovie
        self.time = 0
        self.updateRate=60
        self.timeToUpdate=60
        
        # create movieId to list of server mapping <int, vector<int>>
        self.movieIdTable = dict()

        # create movieId to list of server in cache mapping {movieId : [list of server]}.
        self.cacheTable = dict()

        # record movies {movieId : movieSize}
        self.movies = dict()
        
        # distribute movies to servers (location and size of movie are randomly distributed)
        self.distributedMovie(movieSizeLowerBound, movieSizeUpperBound)

    def updateTime(self):
        self.time+=1
        for sv in self.serverList: sv.curTime+=1

    def update(self):
        # update ranking and cache for each server
        for sv in self.serverList:
            sv.updateRanking()
            sv.updataCache()

        # update cacheTable
        self.cacheTable = dict()
        for movieId in self.movieIdTable:
            for sv in self.movieIdTable[movieId]:
                if movieId in sv.id2CacheIdx:
                    if not movieId in self.cacheTable:
                        self.cacheTable[movieId]=[]
                    self.cacheTable[movieId].append(sv)

        # replicate top ranking movies.
        self.replicateMovie()
        self.timeToUpdate+=self.updateRate

    def replicateMovie(self):
        for sv in self.serverList:
            hotMovieId=sv.rank[0]
            svId = random.randint(0, self.numberOfServer)
            self.serverList[svId].insertMovie(hotMovieId, self.movies[hotMovieId])

    def distributedMovie(self, movieSizeLowerBound, movieSizeUpperBound):
        for i in self.numberOfMovie:
            sv = random.randint(0, self.numberOfServer)

            movieSize=random.randint(movieSizeLowerBound, movieSizeUpperBound)

            # insert the movie to the appropraite server.
            while not self.serverList[sv].insertMovie(i, movieSize):
                sv = random.randint(0, self.numberOfServer)

            # record the movie
            self.movies[i]=movieSize
            
            # record in movieIdTable
            self.movieIdTable[i] = [sv]

            # if the movie is in the cache, record it in self.cacheTable.
            if i in self.serverList[sv].id2CacheIdx:
                self.cacheTable[i] = [sv]
        
    
    def updateLoad(self):
        hasLoad = False
        
        for i in self.numberOfServer:
            if(self.serverList[i].updateLoad() > 0):
                hasLoad = True
                
        return hasLoad
    
    def getNumberOfServer(self):
        return self.numberOfServer
    
    def getDuplicatedRate(self):
        cnt = 0
        for it in self.movieIdTable.values():
            cnt += it
        return cnt/self.movieIdTable.size()
    
    
    def movieRequest(self, movieID, load):
        # Check if the cache in the server has the requested movie
        if movieID in self.cacheTable:
            minload=sys.maxsize
            target_sv=None
            # Get the server that has minimum load
            for sv in self.cacheTable[movieID]:
                if sv.load < minload:
                    minload=sv.load
                    target_sv=sv
            if not target_sv == None and target_sv.accessMovie(movieID, load, 30*load):
                return True

        # Check if any server could handle the requested movie
        minload=sys.maxsize
        target_sv=None
        # Get the server that has minimum load
        for sv in self.movieIdTable[movieID]:
            if sv.load < minload:
                minload=sv.load
                target_sv=sv
        if not target_sv == None and target_sv.accessMovie(movieID, load, load):
                return True
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
        # {movidId: [server1, server2, ...]}, servers that own the movies 

        # update the cache table after updateRanking in server


    # main: 
        # send movieRequest to loadbalancingManager (number of movie, number of server)
    
    # duplication
        # server crash
        # request >= threshold / load >= threshold
        
    # de-replicate
        # number of request in specific time interval 
        
    # cache access time 1
    # disk access time 30
    # request access time 1 
        
            
        
        
        
        
