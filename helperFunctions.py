import matplotlib
matplotlib.use('TKAgg')
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def lowPass(channel):
	b, a = signal.butter(8, 0.125)
	y = signal.filtfilt(b, a, channel, padlen=21)

	return y