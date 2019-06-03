#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from numpy.random import normal as norm

class utils:
    def gaussianSample(lower, upper):
        dis = upper-lower
        ans = int(norm((lower+upper)/2, dis/6))
        if ans >= upper: ans = upper-1
        if ans < lower: ans = lower
        return ans

