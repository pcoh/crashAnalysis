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


def downSampleChannel(channel, oldSampleRate, newSampleRate, firstIndex):
	stepSize = int(oldSampleRate/newSampleRate)
	newChannel = np.zeros([1])
	for x in range(0, int(len(channel)/stepSize-1)):
		# print(channel[firstIndex + x*stepSize])
		newChannel = np.append(newChannel, channel[firstIndex + x*stepSize])
		
	newChannel = np.delete(newChannel, 0)
	return newChannel
	