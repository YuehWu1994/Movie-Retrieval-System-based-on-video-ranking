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
    p.add('--debug', type=bool, required=False, default=False, help="Print current time and load status if debug is set to true")
    args = p.parse_args()
    return args


def one_test(args):
    ms = MS(args.numServer, args.numMovie, args.movieSizeLowerBound, args.movieSizeUpperBound, args.debug)

    req = args.numRequest
    for i in range(req):
        if(args.debug): print("Request: ", i)
        
        # update loadBalanceManager
        if ms.time >= ms.timeToUpdate: ms.update()
        while not ms.movieRequest(random.randrange(0, args.numMovie), ut.gaussianSample(1, args.loadUpperBound)):
            ms.updateTime()
            ms.updateLoad()
        ms.updateTime()
        
        if(args.debug): print('\n')

    while ms.updateLoad(): ms.updateTime()
        
    print("Take ", ms.time, " time unit to finish ", req, " movie requests")    
    return ms.time

    

if __name__ == "__main__": 
    args = _parse_args()
    numberOfTest = 10
    t = []
    
    for i in range(numberOfTest):
        t.append(one_test(args))
    
    t = np.array(t)

    print("Average access time: ", (np.sum(t) - np.min(t) - np.max(t)) / (numberOfTest-2))
