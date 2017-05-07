import matplotlib
matplotlib.use('TKAgg')
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def lowPass(channel, order=2, f_crit=0.25):
	b, a = signal.butter(order, f_crit)
	y = signal.filtfilt(b, a, channel, padlen=21)

	return y