#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from numpy.random import normal as norm
from scipy.stats import uniform
from scipy.stats import expon

class utils:
    def gaussianSample(lower, upper):
        dis = upper-lower
        ans = int(norm((lower+upper)/2, dis/6))
        if ans >= upper: ans = upper-1
        if ans < lower: ans = lower
        return ans
    
    def uniformSample(n, start, width):
        data_uniform = uniform.rvs(size=n, loc = start, scale=width)
        return data_uniform
    
    def expSample(n, lower, upper):
        data_exp = expon.rvs(scale=1,loc=lower,size=n)
        mx = np.max(data_exp)
        data_exp = data_exp * (upper/mx)
        return data_exp