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