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
from utils import utils as ut

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



    

if __name__ == "__main__": 
    args = _parse_args()
    lbm = LBM(args.numServer, args.numMovie, args.movieSizeLowerBound, args.movieSizeUpperBound)

    req = args.numRequest
    for i in range(req):
        print("Request: ", i)
        
        # update loadBalanceManager
        if lbm.time >= lbm.timeToUpdate: lbm.update()
        while not lbm.movieRequest(random.randrange(0, args.numMovie), ut.gaussianSample(1, args.loadUpperBound)):
            lbm.updateTime()
            lbm.updateLoad()
        lbm.updateTime()
        
        print('\n')

    while lbm.updateLoad(): lbm.updateTime()
        
    print("Take ", lbm.time, " time unit to finish ", req, " movie requests")