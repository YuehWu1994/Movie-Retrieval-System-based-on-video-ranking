#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Basic unit of size: Megabyte
# Basic unit of time: s
# Disk throughput: 200MB/s
# Cache throughput: 17GB/s
# movie 1GB ~ 5GB

import random
import configargparse
from LoadBalancingManager import LoadBalancingManager as LBM

def _parse_args():
    p = configargparse.ArgParser()
    p.add('-c', '--config',required=False, is_config_file=True, help='config file path')
    p.add('--numServer',type=int, required=False, default=2, help='number of server')
    p.add('--numMovie', type=int, required=False, default=30, help="number of movie")
    p.add('--numRequest', type=int, required=False, default=30, help="number of movie access request")
    
    p.add('--movieSizeUpperBound', type=int, required=False, default=5000, help="upper bound of requesting load")
    p.add('--movieSizeLowerBound', type=int, required=False, default=1000, help="lower bound of requesting load")
    p.add('--loadUpperBound', type=int, required=False, default=200, help="upper bound of requesting load")
    args = p.parse_args()
    return args

def _initial_reqs(numRequest,numMovie,timeUpperBound,loadUpperBound):
    reqs = dict()
    for i in range(numRequest):
        requestTime = random.randrange(0,timeUpperBound)
        requestMovie = random.randrange(0,numMovie)
        requestLoad = random.randrange(1,loadUpperBound)
        if requestTime in reqs:
            list = reqs[requestTime]
            tuple = (requestMovie,requestLoad)
            list.append(tuple)
            reqs[requestTime] = list
        else :
            list = []
            tuple = (requestMovie,requestLoad)
            list.append(tuple)
            reqs[requestTime] = list
    return reqs
if __name__ == "__main__": 
    args = _parse_args()
    lbm = LBM(args.numServer, args.numMovie, args.movieSizeLowerBound, args.movieSizeUpperBound)
    reqs = _initial_reqs(args.numRequest,args.numMovie,1000,args.loadUpperBound)

    i = 0
    while len(reqs) > 0 :
        if lbm.time >= lbm.timeToUpdate: lbm.update()
        if lbm.time in reqs:
            req_list = reqs[lbm.time]
            for req in req_list:
                # update loadBalanceManager
                
                if not lbm.movieRequest(req[0], req[1]):
                    if lbm.time+1 in reqs:
                        list = reqs[lbm.time+1]
                        tuple = (req[0], req[1])
                        list.append(tuple)
                        reqs[lbm.time+1] = list
                    else :
                        list = []
                        tuple = (req[0], req[1])
                        list.append(tuple)
                        reqs[lbm.time+1] = list 
                    continue
                print("Request: ", i)
                i+=1
            print('\n')
            del reqs[lbm.time]
        lbm.updateTime()
        lbm.updateLoad()
        
        
    while lbm.updateLoad(): lbm.updateTime()
        
    print("Take ", lbm.time, " time unit to finish ", i, " movie requests")
