#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import heapq
import functools

# server
    # declare cache list
    # which movies are in the cache
    # update cache list in specific time interval
    
    ## means I added
    
class Server:
    def __init__(self, movieCapacity, serverDiskCapacity, loadCapacity, t):
        self.loadCapacity = loadCapacity                # upper bound of load
        self.serverDiskCapacity = serverDiskCapacity    # upper bound of disk size 
        self.movieCapacity = movieCapacity              # upper bound of number of movie 
        self.serverCacheCapacity = 10000               ## upper bound of cache size
        self.movieCacheCapacity = 10                   ## upper bound of number of movie 
        
        self.load = 0                                   # current load
        self.totalSize = 0                     
        self.totalCacheSize = 0                        ##
        self.numberOfMovie = 0
        self.numberOfCacheMovie = 0                    ##
        self.cacheDiskSpeedRatio = 30                   # assuem cache transmission speed is 30 times faster than disk
        
        self.curTime = t
        self.q = []                                     # use queue to store accessing time
        
        self.id2Idx = dict()                            # map movie id to array index 
        self.idx2Id = [0] * movieCapacity               # map array index to movie id  
        self.accessReq = [0] * movieCapacity            # number of access
        self.rank = []                                  # ranking of movie 
        self.sizeOfMovie = [0] * movieCapacity          # size of each movie
        self.bandwidth = [0] * movieCapacity            # bandwidth of each movie
        self.aveSizeVideo = 0                           # average size of video
        self.aveBandwidth = 0                           # average bandwidth of video
        
        self.id2CacheIdx = dict()                       ## map movie id to array cache index
        self.idx2CacheId = [0] * self.movieCacheCapacity     ## map array cache index to movie id 
        self.accessCacheReq = [0] * self.movieCacheCapacity  ## number of access
        self.cacheRank = []                             ## ranking of movie 
        self.sizeOfCacheMovie = [0] * self.movieCacheCapacity## size of each movie
        self.cachebandwidth = [0] * self.movieCacheCapacity  ## bandwidth of each movie
        self.aveCacheSizeVideo = 0                      ## average size of video in cache
        self.aveCacheBandwidth = 0                      ## average bandwidth of video in cache
        
        
        
    
    # assign movie to this server
    def insertMovie(self, movieId, movieSize):
        
        ## if the movie already exists in the server
        if movieId in self.id2Idx.keys() or movieId in self.id2CacheIdx.keys():
            return False
        
        ## if  cache has space 
        if self.numberOfCacheMovie < self.movieCacheCapacity and self.numberOfMovie < self.movieCapacity and self.aveCacheSizeVideo * self.numberOfCacheMovie + movieSize <= self.serverCacheCapacity:
            self.insertMovieInCache(movieId, movieSize)
            return True
        
        # if exceed the movie capacity and total length of movie
        if self.numberOfMovie >= self.movieCapacity or self.aveSizeVideo * self.numberOfMovie + movieSize > self.serverDiskCapacity:
            return False
        
        self.id2Idx[movieId] = self.numberOfMovie 
        self.idx2Id[self.numberOfMovie] = movieId
        
        self.rank += [movieId]
        self.sizeOfMovie[self.numberOfMovie] = movieSize
        
        # update average size of movie and average bandwidth
        self.aveSizeVideo = (self.aveSizeVideo * self.numberOfMovie + movieSize) / (self.numberOfMovie + 1)
        self.aveBandwidth = (self.aveBandwidth * self.numberOfMovie) / (self.numberOfMovie + 1)
        
        self.numberOfMovie += 1
        
        
        return True
    
    def insertMovieInCache(self, movieId, movieSize):
        ## First In First cache 
        self.id2CacheIdx[movieId] = self.numberOfCacheMovie 
        self.idx2CacheId[self.numberOfCacheMovie] = movieId
        
        self.cacheRank += [movieId]
        self.sizeOfMovie[self.numberOfCacheMovie] = movieSize
        
        ## update average size of movie and average bandwidth in cache
        self.aveCacheSizeVideo = (self.aveCacheSizeVideo * self.numberOfCacheMovie + movieSize) / (self.numberOfCacheMovie + 1)
        self.aveCacheBandwidth = (self.aveCacheBandwidth * self.numberOfCacheMovie) / (self.numberOfCacheMovie + 1)
        
        self.numberOfMovie += 1
        self.numberOfCacheMovie += 1
        print("cache", self.numberOfCacheMovie)
        
    
    # sort the ranking
    def sortRankingAlg(self, x, y):
        xIdx = self.id2Idx[x]
        yIdx = self.id2Idx[y]
        return self.accessReq[xIdx] > self.accessReq[yIdx] or (
                self.accessReq[xIdx] == self.accessReq[yIdx] and self.bandwidth[xIdx] > self.bandwidth[yIdx])
    def sortCacheRankingAlg(self, x, y):
        xIdx = self.id2CacheIdx[x]
        yIdx = self.id2CacheIdx[y]
        return self.accessCacheReq[xIdx] > self.accessCacheReq[yIdx] or (
                self.accessCacheReq[xIdx] == self.accessCacheReq[yIdx] and self.cachebandwidth[xIdx] > self.cachebandwidth[yIdx])
    
    def updateRanking(self):
        if self.numberOfMovie == 0 or self.aveBandwidth == 0:
            return False
        
        # update bandwidth
        for i in range(self.numberOfMovie):
            self.bandwidth[i] = self.sizeOfMovie[i] * 100 / self.aveSizeVideo * self.aveBandwidth
        
        self.rank=sorted(self.rank, key=functools.cmp_to_key(self.sortRankingAlg))
        self.cacheRank=sorted(self.cacheRank, key=functools.cmp_to_key(self.sortCacheRankingAlg))
        return True
        
    
    # access the movie by bandwidth and movieID
    def accessMovie(self, movieId, bandwidth, loadSpeed):
        ## if exceed the load
        if self.load + loadSpeed > self.loadCapacity:
            return False
        
        ## if the movie does exist in the server cache
        if movieId in self.id2CacheIdx.keys():
            self.accessCacheMovie(movieId, loadSpeed, loadSpeed)
            return True
        ## if the movie doesn't exist in the server
        if movieId not in self.id2Idx.keys():
            return False
    
        
        movieIdx = self.id2Idx[movieId]
        
        heapq.heappush(self.q, (self.curTime + int(self.sizeOfMovie[movieIdx]/loadSpeed)+1, loadSpeed))
        
        self.load += loadSpeed
        self.accessReq[movieIdx] += 1
        self.bandwidth[movieIdx] += bandwidth
        self.aveBandwidth = self.aveBandwidth + bandwidth/self.numberOfMovie
        return True
    
    
    def accessCacheMovie(self, movieId, bandwidth, loadSpeed):
        movieIdx = self.id2CacheIdx[movieId]
        
        #print(self.sizeOfCacheMovie)
        heapq.heappush(self.q, (self.curTime + int(self.sizeOfCacheMovie[movieIdx]/loadSpeed*self.cacheDiskSpeedRatio)+1, loadSpeed))
        
        self.load += loadSpeed
        self.accessCacheReq[movieIdx] += 1
        self.cachebandwidth[movieIdx] += bandwidth
        self.aveCacheBandwidth = self.aveCacheBandwidth + bandwidth/self.numberOfCacheMovie
        
        
    def updateLoad(self):
        while len(self.q) > 0 and self.q[0][0] <= self.curTime:
            self.load -= self.q[0][1]
            heapq.heappop(self.q)
            
        return len(self.q)
    
    # exchange the lowest rank movie in cache with the highest rank movie in disk
    def updateCache(self):
        if(len(self.rank) == 0 or len(self.cacheRank) == 0):
            return
        
        ## x,y are movie ID
        x = self.rank[0] 
        y = self.cacheRank[self.numberOfCacheMovie-1]
        
        self.rank[0] = y
        self.cacheRank[self.numberOfCacheMovie-1] = x
        
        ## index x & Index y
        idxx = self.id2Idx[x]
        idxy = self.id2CacheIdx[y]
        del self.id2Idx[x]
        del self.id2CacheIdx[y]
        self.id2Idx[y] = idxx
        self.id2CacheIdx[x] = idxy
        
        temp = self.idx2Id[idxx]
        self.idx2Id[idxx] = self.idx2CacheId[idxy]
        self.idx2CacheId[idxy] = temp          #peng
        
        temp = self.accessReq[idxx]
        self.accessReq[idxx] = self.accessCacheReq[idxy]
        self.accessCacheReq[idxy] = temp       #peng
        
        temp = self.sizeOfMovie[idxx]
        self.sizeOfMovie[idxx] = self.sizeOfCacheMovie[idxy]
        self.sizeOfCacheMovie[idxy] = temp     #peng
        
        temp = self.bandwidth[idxx]
        self.bandwidth[idxx] = self.cachebandwidth[idxy]
        self.cachebandwidth[idxy] = temp       #peng
