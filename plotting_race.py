import nidaqmx
import numpy as np
import time
import matplotlib.pyplot as plt

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

samples = 100
rate = 10000
channel = 'Dev3/ai0'
nmax = 5

task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan(channel)

def get_ydata():
    task.timing.cfg_samp_clk_timing(rate, 
        # sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS, 
        samps_per_chan=samples)
    r = task.read(number_of_samples_per_channel=samples)
    return np.array(r)

## matplotlib
fig, ax = plt.subplots()
line, = ax.plot(np.linspace(-10, 10, samples))
plt.show(block=False)
fig.canvas.draw()

tstart = time.time()
num_plots = 0
while time.time()-tstart < nmax:
    line.set_ydata(get_ydata())
    fig.canvas.draw()
    fig.canvas.flush_events()
    num_plots += 1
print(num_plots/nmax)

## qtgraph
app = QtGui.QApplication([])

pW = pg.plot()
pW.setRange(QtCore.QRectF(0, -10, samples, 20))
curve = pW.plot()

tstart = time.time()
num_plots = 0
while time.time()-tstart < nmax:
    curve.setData(get_ydata())
    app.processEvents()
    num_plots += 1
print(num_plots/nmax)
task.close()

app.exec_()