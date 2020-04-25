import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import sys

theTitle = "My first plot"
y = [0, 2, 3, 4, 2]
x = range(0, 5)

plt = pg.plot()
plt.addLegend()

plt.setLabel('left', 'Value', units='V')
plt.setLabel('bottom', 'Time', units='s')

c1 = plt.plot(x, y, pen='b', name='money')

y = [0, 1, 5, 4, 2, 9]
x = range(0, 6)

c1 = plt.plot(x, y, pen='r', name='money')

pg.QtGui.QApplication.exec_()