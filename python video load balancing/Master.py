#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from server import Server
import random
import sys
from utils import utils as ut

class Master:
    def __init__(self, numberOfServer, numberOfMovie, movieSizeLowerBound, movieSizeUpperBound, cacheDiskSpeedRatio, debug, ranking):
        # debug mode, ranking
        self.debug = debug
        self.ranking = ranking
        
        self.cacheDiskSpeedRatio = cacheDiskSpeedRatio
        self.serverList = []
        self.numberOfServer = 0
        
        for i in range(numberOfServer):
            self.createServer()
            
        self.numberOfMovie = numberOfMovie
        self.time = 0
        self.updateRate=10
        self.timeToUpdate=10
        self.replicateTime = 0
        
        # create movieId to list of server mapping <int, vector<int>>
        self.movieIdTable = dict()

        # create movieId to list of server in cache mapping {movieId : [list of server]}.
        self.cacheTable = dict()

        # record movies {movieId : movieSize}
        self.movies = dict()
        
        # distribute movies to servers (location and size of movie are randomly distributed)
        self.distributedMovie(movieSizeLowerBound, movieSizeUpperBound)
        
        self.requestFailCnt = 0
        self.diskTrans = 0
        self.cacheTrans = 0
        self.diskTry = 0
        self.cacheTry = 0
        
    

    def updateTime(self):
        self.time +=1
        for sv in self.serverList: sv.curTime+=1
        
        if self.debug: print("Current Time is: ", self.time)

    def update(self):        
        
        if self.ranking:
            # update ranking and cache for each server          
            for sv in self.serverList:
                #print("updata at time: ",self.time)
                sv.updateRanking()
                sv.updateCache()
    
            
            # update cacheTable
            self.cacheTable = dict()
            for movieId in self.movieIdTable:
                for sv in self.movieIdTable[movieId]:
                    if movieId in self.serverList[sv].id2CacheIdx:
                        if not movieId in self.cacheTable:
                            self.cacheTable[movieId]=[]
                        self.cacheTable[movieId].append(sv)
        
        
        
        # replicate top ranking movies.
        for i in range(1):
            self.replicateMovie()
        self.timeToUpdate+=self.updateRate
        
    def createServer(self):
        sv = Server(20, 50000, 500, self.cacheDiskSpeedRatio, 0, self.debug)
        self.serverList.append(sv)
        self.numberOfServer += 1

    def replicateMovie(self):
        hotMovieId = 0
        for sv in self.serverList:
            if sv.load <= 450:
                continue
            
            if len(sv.cacheRank) != 0:
                hotMovieId = sv.cacheRank[0]
            elif len(sv.rank) != 0: 
                hotMovieId=sv.rank[0]
            else:
                continue
                                   
            svId = random.randrange(0, self.numberOfServer)
            if(self.serverList[svId].insertMovie(hotMovieId, self.movies[hotMovieId])):
                # insert in movieIdTable and cache table
                self.movieIdTable[hotMovieId].append(svId)
            
                if hotMovieId in self.serverList[svId].id2CacheIdx:
                    self.cacheTable[hotMovieId].append(svId)           
            
                self.replicateTime += 1

    def distributedMovie(self, movieSizeLowerBound, movieSizeUpperBound):
        for i in range (self.numberOfMovie):
            sv = random.randrange(0, self.numberOfServer)

            movieSize = ut.gaussianSample(movieSizeLowerBound, movieSizeUpperBound)

            if self.debug: print("Movie ", i, " is located in server: ", sv)
            # insert the movie to the appropraite server.
            cnt = 0
            while not self.serverList[sv].insertMovie(i, movieSize):                    
                sv = random.randrange(0, self.numberOfServer)
                cnt += 1
                
                # create new server
                if cnt == self.numberOfServer:
                    self.createServer()
                    sv = self.numberOfServer-1

            # record the movie
            self.movies[i]=movieSize
            
            # record in movieIdTable
            self.movieIdTable[i] = [sv]

            # if the movie is in the cache, record it in self.cacheTable.
            if i in self.serverList[sv].id2CacheIdx:
                self.cacheTable[i] = [sv]
        
        if self.debug: print("=====Distribute Movie: DONE===== \n")
        
    
    def updateLoad(self):
        hasLoad = False
        
        for i in range (self.numberOfServer):
            unFinishLoad = self.serverList[i].updateLoad()
            if(unFinishLoad > 0):
                if self.debug: print("server ", i, " still has ", unFinishLoad, " load")
                hasLoad = True
        
        if self.debug: print("\n")        
        return hasLoad
    
    def getNumberOfServer(self):
        return self.numberOfServer
    
    def getDuplicatedRate(self):
        cnt = 0
        for it in self.movieIdTable.values():
            cnt += it
        return cnt/self.movieIdTable.size()
    
    
    def movieRequest(self, movieID, load):
        if self.debug: print("Request movie ", movieID, ". Load speed is: ", load)
        
        # Check if the cache in the server has the requested movie
        if movieID in self.cacheTable:
            minload=sys.maxsize
            target_sv=None
            # Get the server that has minimum load
            for sv in self.cacheTable[movieID]:
                if self.serverList[sv].load < minload:
                    minload=self.serverList[sv].load
                    target_sv=sv
            if not target_sv == None and self.serverList[target_sv].accessCacheMovie(movieID, load, load):
                if self.debug: print("Server ", target_sv, " use cache to transmit")
                self.cacheTrans += 1
                return True
            self.cacheTry += 1
            

        # Check if any server could handle the requested movie
        minload=sys.maxsize
        target_sv=None
        # Get the server that has minimum load
        for sv in self.movieIdTable[movieID]:
            if self.serverList[sv].load < minload:
                minload=self.serverList[sv].load
                target_sv=sv
        
        
        if not target_sv == None and self.serverList[target_sv].accessMovie(movieID, load, load):
            if self.debug: print("Server ", target_sv, " use disk to transmit")
            self.diskTrans += 1
            return True
        self.diskTry += 1
        
        self.requestFailCnt += 1
        
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
        
            