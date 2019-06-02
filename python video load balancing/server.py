#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import numpy as np
import heapq


class Server:
    def __init__(self, movieCapacity, serverDiskCapacity, loadCapacity, t):
        self.loadCapacity = loadCapacity              # upper bound of load
        self.serverDiskCapacity = serverDiskCapacity  # upper bound of disk size 
        self.movieCapacity = movieCapacity            # upper bound of number of movie 
        
        self.load = 0                                 # current load
        self.totalSize = 0                     
        self.numberOfMovie = 0
        
        self.curTime = t
        self.q = []                                   # use queue to store accessing time
        
        self.id2Idx = dict()                          # map movie id to array index 
        self.idx2Id = [0] * movieCapacity             # map array index to movie id   
        self.accessReq = [0] * movieCapacity          # number of access
        self.rank = []                                # ranking of movie 
        self.sizeOfMovie = [0] * movieCapacity        # size of each movie
        self.bandwidth = [0] * movieCapacity          # bandwidth of each movie
        self.aveSizeVideo = 0                         # average size of video
        self.aveBandwidth = 0                         # average bandwidth of video
        
        
        
        
    
    # assign movie to this server
    def insertMovie(self, movieId, movieSize):
        # if exceed the movie capacity and total length of movie
        if self.numberOfMovie == self.movieCapacity or self.aveSizeVideo * self.numberOfMovie + movieSize > self.serverDiskCapacity:
            return False
        
        # if the movie already exists in the server
        if movieId in self.id.keys():
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
    
    # sort the ranking
    def sortRankingAlg(self, x, y):
        xIdx = self.id2Idx[x]
        yIdx = self.id2Idx[y]
        return self.accessReq[xIdx] > self.accessReq[yIdx] or (
                self.accessReq[xIdx] == self.accessReq[yIdx] and self.bandwidth[xIdx] > self.bandwidth[yIdx])
    
    def updateRanking(self):
        if self.numberOfMovie == 0 or self.aveBandwidth == 0:
            return False
        
        # update bandwidth
        for i in range(self.numberOfMovie):
            self.bandwidth[i] = self.sizeOfMovie[i] * 100 / self.aveSizeVideo * self.aveBandwidth
        
        sorted(self.rank, cmp=self.sortRankingAlg)
        return True
        
    
    # access the movie by bandwidth and movieID
    def accessMovie(self, movieId, bandwidth, load):
        # if the movie doesn't exist in the server
        if movieId in self.id.keys():
            return False
        
        # if exceed the load
        if self.load + load > self.loadCapacity:
            return False
    
        
        movieIdx = self.id2Idx[movieId]
        
        heapq.heappush((self.q, self.curTime + int(self.sizeOfMovie[movieIdx]/load)+1), load)
        
        self.load += load
        self.accessReq[movieIdx] += 1
        self.bandwidth[movieIdx] += bandwidth
        self.aveBandwidth = self.aveBandwidth + bandwidth/self.numberOfMovie
        return True
    
    def updateLoad(self):
        while not self.q.empty() and self.q[0] <＝ self.curTime:
            self.load -= self.q[0][1]
            heapq.heappop(self.q)
            
        return self.q.size()
            
        
        
    
