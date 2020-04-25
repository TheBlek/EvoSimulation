import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
import random

fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = plt.plot([],[], lw=3)
global y
y = np.array([])

def init():
    line.set_data([],[])
    return line, 
def animate(i):
    global y
    x = np.linspace(0, i, i * 1000)
    #y = np.sin(2 * np.pi * (x + 0.01 * i))
    y.append(i)
    line.set_data(x,y)
    return line, 
anim = animation.FuncAnimation(fig, animate,init_func=init, frames=200, interval=20)
plt.show()
