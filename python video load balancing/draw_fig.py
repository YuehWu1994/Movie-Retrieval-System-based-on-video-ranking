#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np

x = np.array([10,50,100,500,1000,2000,5000])
y_wRank = np.array([70.0, 368.1, 695.5, 2009.0, 2948.2, 4402.4, 7559.7])
y_woRank = np.array([59.4, 360.16, 561.1, 1762.8, 2685.0, 3942.9, 7256.9])

#y_wRank_Uni = np.array([91.6, 419.5, 475.3, 1815.1, 3205.0, 4291.1, 7677.5])
#y_woRank_Uni = np.array([72.4, 436.0, 480.0, 1827.9, 3064.3, 4122.4, 7398.0])


plt.plot(x, y_wRank, label='Exponential Distribution with ranking')
plt.plot(x, y_woRank, label='Exponential Distribution w/o ranking')

#plt.plot(x, y_wRank_Uni, label='Uniform Distribution with ranking')
#plt.plot(x, y_woRank_Uni, label='Uniform Distribution w/o ranking')


plt.xlabel('number of request')
plt.ylabel('Average Access Time(sec)')

plt.title("Uniform Distribution V.S Exponential Distribution")

plt.legend()

plt.show()

'''
Number of Movie
10,50,100,500,1000, 2000
1048, 1065.9, 1213.7, 2633.7, 3206.5, 2892.9
1045.5, 1049.3, 1169.9, 2114.4, 2492.2, 2531.3

Number of Request
10,50,100,500,1000,2000,5000
70.0, 368.1, 695.5, 2009.0, 2948.2, 4402.4, 7559.7
59.4, 360.16, 561.1, 1762.8, 2685.0, 3942.9, 7256.9

Cache Disk Speed Ratio
10, 30, 50, 80, 100, 200, 300
2783.0, 2980.8, 2741.2, 2775.0, 2811.8, 2904.3, 2719.3
2380.1, 2833.2 2647.3, 2753.8, 2501.0, 2657.9, 2510.1

Distribution
10,50,100,500,1000,2000,5000
70.0, 368.1, 695.5, 2009.0, 2948.2, 4402.4, 7559.7
59.4, 360.16, 561.1, 1762.8, 2685.0, 3942.9, 7256.9

91.6, 419.5, 475.3, 1815.1, 3205.0, 4291.1, 7677.5
72.4, 436.0, 480.0, 1827.9, 3064.3, 4122.4, 7398.0
'''