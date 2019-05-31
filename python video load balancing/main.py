#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Basic unit of size: Megabyte
# Basic unit of time: s
# Disk throughput: 200MB/s
# Cache throughput: 17GB/s

import random
import configargparse
import LoadBalancingManager as LBM

def _parse_args(self):
    p = configargparse.ArgParser()
    p.add('--numServer',required=True, help='number of server')
    p.add('--numMovie', required=True, help="number of movie")
    p.add('--numRequest', required=True, help="number of movie access request")
    
    p.add('--movieSizeUpperBound', required=False, default=5000, help="upper bound of requesting load")
    p.add('--movieSizeLowerBound', required=False, default=1000, help="lower bound of requesting load")
    p.add('--loadUpperBound', required=False, default=500, help="upper bound of requesting load")
    args = p.parse_args()
    return args

if __name__ == "__main__": 
    args = _parse_args()
    lbm = LBM(args.numServer, args.numMovie, args.movieSizeLowerBound, args.movieSizeUpperBound)

    req = args.numRequest
    for i in req:
        LBM.movieRequest(random.randint(0, args.numMovie), random.randint(0, args.loadUpperBound))
        
        
    print("Take " + LBM.t + "time unit to finish " +  req + " movie requests")