import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import os.path
import csv
import numpy as np
from numpy import genfromtxt
import scipy
from helperFunctions import *


# define empty class for data structure:
class Data:
	pass

def checkChannelAvail(channel):
	# dismiss all non-numbers ( NaN):
	numValues = np.extract(np.logical_not(np.isnan(channel)), channel)
	finiteValues = np.extract(np.isfinite(numValues), numValues)
	nonZeros = np.extract(np.nonzero(finiteValues), finiteValues)
	# print ("Numvalues: ", numValues)
	# print ("finiteValues: ", finiteValues)
	# print ("nonZeros: ", nonZeros)
	if len(nonZeros)>0:
		return True
	else:
		return False

# define vehicle class:
class Vehicle(object):

	def __init__(self, VIN):
		self.VIN = VIN
		self.data = Data()
		
		self.make = 'unknown'
		self.model = 'unknown'
	
	def loadData(self):
		fileName = os.getcwd() + '/'+ self.VIN + '.csv'
		if (os.path.isfile(fileName)):
			self.data.isavailable = True
			self.data.raw = genfromtxt(fileName, delimiter=',')
			self.data.time = self.data.raw[1:,0]
			self.data.sampleRate = round((len(self.data.time)-1)/(self.data.time[-1]-self.data.time[0]),2)
			print("startTime :", self.data.time[0])
			print("startTime :", self.data.time[-1])
			print("sampleRate :", self.data.sampleRate)
			self.data.speedometer = self.data.raw[1:,0]
			self.data.parkingSensor_rear = self.data.raw[1:,24]
		else:
			self.data.isavailable = False
			# print("No data available for ", VIN )

	def establishImpactTime(self):
		# if(parking distance sensor signal is available),find time at which the indicated distance of the first sensor becomes (very close to) zero:
		if(checkChannelAvail(self.data.parkingSensor_rear)):
			# numValues = np.extract(np.logical_not(np.isnan(self.data.parkingSensor_rear)), self.data.parkingSensor_rear)
			# finiteValues = np.extract(np.isfinite(numValues), numValues)
			# time_at_numValues = np.extract(np.logical_not(np.isnan(self.data.parkingSensor_rear)), self.data.time)
			# time_at_finiteValues =  np.extract(np.isfinite(numValues), time_at_numValues)
			
			
			# parkingSensor_rear_smooth1 = lowPass(finiteValues, f_crit= 0.25)
			# parkingSensor_rear_smooth2 = lowPass(finiteValues, f_crit= 0.4)
			# plt.plot(self.data.parkingSensor_rear)
			# plt.plot(parkingSensor_rear_smooth1)
			# plt.plot(parkingSensor_rear_smooth2)
			# plt.show()

			dist_Thresh = 0.005
			for idx, x in np.ndenumerate(self.data.parkingSensor_rear):
				if (x < dist_Thresh):
					self.data.impactTime = self.data.time[idx]
					break
			print("ImpactTime: ", self.data.impactTime )

		# elif (brakeOn/Off signal is available):
		# 	if(brake ==0):
		# 		find time at which deceleration becomes greater that possible from coast-down
		# 		(need to consider gradient of road??)
		# 	else:
		# 		if not binary:
		# 			find time at which deceleration becomes greater than what is caused by braking	==> simple vehicle dynamics model (based on historic data)
		# 		else:
		# 			if (deceleration greater than full braking would caused)

		# 		else:
		# 			Fallback solution
		
		
		# elif high impact:
		# 	find time at which abs(acel_X) becomes greater than what could be achieved by braking.

		# 	check against (RELEVANT impact accelerometer data is available):
		# 	find time at which accel from impact sensor starts to diverge from accel of vehicle.
		# 	only relevant if large deformations in crash structure present (sensor sits on crash-beam)
			

		# else:
		# 	Fallback solution:
		# 	analyse shape of acceleration (more gradual if caused by braking)
		# 	if pitch angle available: 
		# 			if deceleration > pitch angle indicates ==> assumed impact (requires simple vehicle model)
		# 		is yaw rate relevant?

		# 	over time, a ML model could learn to identify time of impact from accelerometer data (training data is data that has clear signal (e.g. paking sensor))

# define accident class:
class Accident(object):

	def __init__(self, VINList, category):
		self.category = category
		self.involvedVehicles = VINList

	def runAnalysis(self):
		if(self.category == "ParkingLot"):
			print("running analysis")
			for vehicle in accident.involvedVehicles:
				if (vehicle.data.isavailable ==True):
					print(vehicle.VIN)
					vehicle.establishImpactTime()

		else:
			print("unable to analyse this type of accident")

	

		



# Create instances of Vehicle:		
car1 = Vehicle('1C4GJ45331B133332')
car1.loadData()

car2 = Vehicle('1J4FT58L2KL609051')
car2.loadData()


# create instance of accident with involved vehicles:
accident = Accident([car1, car2], "ParkingLot")

accident.runAnalysis()




# if category=="ParkingLot":

# 	establishImpactTime()
# 	checkStandstill()
# 	checkStandstillDuration()
# 	checkHonk()
# 	checkFirstMover()
# 	checkBackingSpeed()
# 	print(channel0)
# 	print(channel1)
# 	print(channel2)


