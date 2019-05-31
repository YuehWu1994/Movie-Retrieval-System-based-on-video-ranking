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
            
        
        
        
        
