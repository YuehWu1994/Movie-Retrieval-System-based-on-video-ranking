#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Basic unit of size: Megabyte
# Basic unit of time: s
# Disk throughput: 200MB/s
# Cache throughput: 17GB/s
# movie 1GB ~ 5GB

import random
import configargparse
from Master import Master as MS
from utils import utils as ut
import numpy as np

def _parse_args():
    p = configargparse.ArgParser()
    p.add('-c', '--config',required=False, is_config_file=True, help='config file path')
    p.add('--numServer',type=int, required=False, default=2, help='number of server')
    p.add('--numMovie', type=int, required=False, default=30, help="number of movie")
    p.add('--numRequest', type=int, required=False, default=30, help="number of movie access request")
    
    p.add('--movieSizeUpperBound', type=int, required=False, default=5000, help="upper bound of movie size")
    p.add('--movieSizeLowerBound', type=int, required=False, default=1000, help="lower bound of movie size")
    p.add('--loadUpperBound', type=int, required=False, default=200, help="upper bound of requesting load")
    p.add('--cacheDiskSpeedRatio', type=int, required=False, default=30, help="speed ratio of cache and disk")
    p.add('--debug', type=bool, required=False, default=False, help="Print current time and load status if debug is set to true")
    p.add('--requestDistribution', type=str, required=False, default="Normal", help="Apply which probability distribution models on movie request")
    args = p.parse_args()
    return args


def one_test(args):
    ms = MS(args.numServer, args.numMovie, args.movieSizeLowerBound, args.movieSizeUpperBound, args.cacheDiskSpeedRatio, args.debug)
    req = args.numRequest
    
    
    sample = []
    if args.requestDistribution == "Normal" :
        # Assume movie requests are uniformly distributed
        sample = ut.uniformSample(req, 0, args.numMovie-1)
    else: 
        # Some popular movies have extensive request. Apply exponential distribution on popularity 
        sample = ut.expSample(req, 0, args.numMovie-1)
        
    for i in range(req):
        if(args.debug): print("Request: ", i)
        
        # update loadBalanceManager
        if ms.time >= ms.timeToUpdate: ms.update()
        while not ms.movieRequest(round(sample[i]), ut.gaussianSample(1, args.loadUpperBound)):
            ms.updateTime()
            ms.updateLoad()
        ms.updateTime()
        
        if(args.debug): print('\n')

    while ms.updateLoad(): ms.updateTime()
        
    print("Take ", ms.time, " time unit to finish ", req, " movie requests")    
    return ms.time, ms.replicateTime

    

if __name__ == "__main__": 
    args = _parse_args()
    numberOfTest = 10
    time, replicate = [], []
    
    for i in range(numberOfTest):
        t, rep = one_test(args)
        time.append(t)
        replicate.append(rep)
    
    time = np.array(time)
    replicate = np.array(replicate)

    print("Average access time: ", (np.sum(time) - np.min(time) - np.max(time)) / (numberOfTest-2))
    print("Average replication: ", (np.sum(replicate) - replicate[np.argmin(time)] - replicate[np.argmax(time)]) / (numberOfTest-2))
