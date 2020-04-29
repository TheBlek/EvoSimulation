import random
import pyqtgraph as pg
import sys
import numpy as np
import math

def noise():
    mapsize = 256
    map = []
    mapFO = []
    for i in range(mapsize // 4):
        mapFO.append(random.randint(-1, 2))
    for i in range(mapsize):
        d = int(i // (mapsize / 4) + 1)
        map.append((random.randint(-1, 1) / 2 + mapFO[d]) / 2)
    return map

def new_noise():
    mapsize = 256
    map = []
    mapFO = []
    for i in range(mapsize // 4):
        mapFO.append(random.randint(-1, 2))
    mapFO = smoother(mapFO, 0.6)
    for i in range(mapsize):
        d = int(i // (mapsize / 4) + 1)
        map.append((random.randint(-1, 1) / 2 + mapFO[d]) / 2)
    return map

def smoother(map, sm_coeff):
    for i in range(len(map) - 1):
        if map[i + 1] - map[i] > 0.2:
            map[i + 1] -= sm_coeff * (map[i + 1] - map[i])
            map[i] += sm_coeff * (map[i + 1] - map[i])

        if map[i] - map[i + 1] > 0.2:
            map[i + 1] += sm_coeff * (map[i] - map[i + 1]) 
            map[i] -= sm_coeff * (map[i] - map[i + 1])
    return map

def otherSmoother(map, sm_coeff):
    new_map = []
    for i in range(len(map) - sm_coeff):
        summ = 0
        for j in range(sm_coeff):
            summ += map[i + j]
        new_map.append(summ / sm_coeff)
    for i in range(sm_coeff):
        summ = 0
        for j in range(sm_coeff - i):
            summ += map[-sm_coeff + j]
        new_map.append(summ / (sm_coeff - i))
    return new_map


plt = pg.plot()
x = np.linspace(0, 256, 256)
plt.addLegend()
map = noise()
map2 = new_noise()
#plt.plot(x, map, pen='y', name='std noise')
#plt.plot(x, map2, pen='g', name='new noise')
#plt.plot(x, smoother(smoother(map, 0.6), 0.6), pen='g', name='double 0.6')
#plt.plot(x, smoother(otherSmoother(smoother(smoother(map, 0.6), 0.6), 2), 0.6), pen='b', name='0.6 new 2 after double 0.6')
#plt.plot(x, smoother(otherSmoother(smoother(smoother(map, 0.6), 0.6), 3), 0.6), pen='r', name='0.6 new 3 after double 0.6')
plt.plot(x, smoother(otherSmoother(smoother(smoother(map, 0.6), 0.6), 4), 0.6), pen='r', name='0.6 new 4 after double 0.6')
plt.plot(x, smoother(otherSmoother(smoother(smoother(map2, 0.6), 0.6), 4), 0.6), pen='g', name='0.6 new 4 after double 0.6')
#plt.plot(x, smoother(smoother(map2, 0.6), 0.6), pen='b', name='new noise after double 0.6')
#plt.plot(x, smoother(otherSmoother(map, 0.6), 0.6), pen='b', name='new 0.6 after 0.6')

if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
    pg.QtGui.QApplication.exec_()