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
from simulator import *
import random
import pickle


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
		self.analytics = Data()
		self.analytics.impactTime = -1
		self.analytics.fullStop = -1
	
	def fetchAccidentData(self, scene):
		if self.VIN == scene.involvedCars[0].VIN:
			return scene.involvedCars[0].datalog
		elif self.VIN == scene.involvedCars[1].VIN:
			return scene.involvedCars[1].datalog
		else:
			print("VIN ", self.VIN, " not found")

	def loadData(self, scene):
		logData = self.fetchAccidentData(scene)
		self.data.isavailable = True
		self.data.time = logData.time
		self.data.sampleRate = round(1/scene.stepSize,2)
		self.data.dist = logData.dist
		self.data.speedometer = logData.speed
		self.data.parkdist_rear = logData.parkdist_rear
		self.data.accel_x = logData.accel_x
		self.data.brakeOn = logData.brakeOn

	def downSampleData(self, newSampleRate):
		downsamplingFactor = self.data.sampleRate/newSampleRate
		if downsamplingFactor % 1 != 0:
			print("Error. Original sample rate needs to be multiple of new sample rate")
		else:
			# print("Downsampling data")
			firstIndex = random.randint(0,downsamplingFactor)
			
			self.data.time = downSampleChannel(self.data.time, self.data.sampleRate, newSampleRate, firstIndex)
			self.data.dist = downSampleChannel(self.data.dist, self.data.sampleRate, newSampleRate, firstIndex)
			self.data.speedometer = downSampleChannel(self.data.speedometer, self.data.sampleRate, newSampleRate, firstIndex)
			self.data.parkdist_rear = downSampleChannel(self.data.parkdist_rear, self.data.sampleRate, newSampleRate, firstIndex)
			self.data.accel_x = downSampleChannel(self.data.accel_x, self.data.sampleRate, newSampleRate, firstIndex)
			self.data.brakeOn = downSampleChannel(self.data.brakeOn, self.data.sampleRate, newSampleRate, firstIndex)
			

	def establishImpactTime(self):
		# if(parking distance sensor signal is available),find time at which the indicated distance of the first sensor becomes (very close to) zero:
		if(checkChannelAvail(self.data.parkdist_rear)):
			# print("park sensor available")
			dist_Thresh = 0.01
			for idx, x in np.ndenumerate(self.data.parkdist_rear):
				if (x < dist_Thresh):
					self.analytics.impactTime = self.data.time[idx]
					# print("ImpactTime: ", self.analytics.impactTime )
					break
				if idx[0] == len(self.data.parkdist_rear)-1 and x>=dist_Thresh:
					# print("No impact occurred")
					self.analytics.impactTime = -1
		# else:
		# 	print("park sensor NOT available or out of range")

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

	def __init__(self, involvedVehicles, category):
		self.category = category
		self.involvedVehicles = involvedVehicles
		self.time = 0

	def runAnalysis(self):
		if(self.category == "ParkingLot"):
			# print("running analysis")
			for vehicle in self.involvedVehicles:
				if (vehicle.data.isavailable ==True):
					# print(vehicle.VIN)
					vehicle.establishImpactTime()
			self.assignGlobalAccidentTime()
			self.checkStandstill()
		else:
			print("unable to analyse this type of accident")

	def assignGlobalAccidentTime(self):
		impactTimes = []
		for vehicle in self.involvedVehicles:
			impactTimes.append(vehicle.analytics.impactTime)
		self.time = min(impactTimes)
	def checkStandstill(self):
		for vehicle in self.involvedVehicles:
			if (vehicle.analytics.impactTime > 0):
				impactTimeIndex = np.where(vehicle.data.time==vehicle.analytics.impactTime)[0]
				# print("impactTimeIndex: ", impactTimeIndex)
				if vehicle.data.speedometer[impactTimeIndex -1] <= 0.001:
					vehicle.analytics.fullStop = 1
				else:
					vehicle.analytics.fullStop = 0


def plotResults(car1, car2):
	fig, ax = plt.subplots(nrows=5,ncols=1)

	ax1 = plt.subplot(5,1,1)
	ax1.title.set_text('Position')
	plt.plot(car1.data.time, car1.data.dist)
	plt.plot(car2.data.time, scene.aisleWidth-car2.data.dist)

	ax2 = plt.subplot(5,1,2)
	ax2.title.set_text('Speed')
	plt.plot(car1.data.time, car1.data.speedometer)
	plt.plot(car2.data.time, car2.data.speedometer)

	ax3 = plt.subplot(5,1,3)
	ax3.title.set_text('Accel X')
	plt.plot(car1.data.time, car1.data.accel_x)
	plt.plot(car2.data.time, car2.data.accel_x)

	ax4 = plt.subplot(5,1,4)
	ax4.title.set_text('Brake On')
	plt.plot(car1.data.time, car1.data.brakeOn)
	plt.plot(car2.data.time, car2.data.brakeOn)

	ax5 = plt.subplot(5,1,5)
	ax5.title.set_text('Park Dist')
	plt.plot(car1.data.time, car1.data.parkdist_rear)
	plt.plot(car2.data.time, car2.data.parkdist_rear)


	plt.show()


# scene = createAccidentData()
# # Create instances of Vehicle:		
# car1 = Vehicle('1C4GJ45331B133332')
# car1.loadData(scene)

# car2 = Vehicle('1J4FT58L2KL609051')
# car2.loadData(scene)


# # create instance of accident with involved vehicles:
# accident = Accident([car1, car2], "ParkingLot")
# accident.runAnalysis()
# print(car1.analytics.fullStop)
# print(car2.analytics.fullStop)

# plotResults(car1, car2)

numRuns = 1000
sampleRateVector = [100,50,10,5,2,1,0.5,0.1]

car1_HitVector = []
car2_HitVector = []
for currSampleRate in sampleRateVector:
	print("calculating samle rate: ", currSampleRate)
	car1_standstillCount_High = 0
	car2_standstillCount_High = 0
	car1_standstillCount_Low =0
	car2_standstillCount_Low = 0
	car1_HitRatio = 0.0
	car2_HitRatio = 0.0
	for x in range(numRuns):
		# print(x)
		# create simulated accident data:
		scene = createAccidentData()

		# Create instances of Vehicle:		
		car1 = Vehicle('1C4GJ45331B133332')
		car1.loadData(scene)

		car2 = Vehicle('1J4FT58L2KL609051')
		car2.loadData(scene)


		# create instance of accident with involved vehicles:
		accident = Accident([car1, car2], "ParkingLot")
		accident.runAnalysis()
		if car1.analytics.fullStop ==1:
			car1_standstillCount_High += 1
		if car2.analytics.fullStop ==1:
			car2_standstillCount_High += 1
		# print("StandStill Car 1: ", car1.analytics.fullStop)
		# print("StandStill Car 2: ", car2.analytics.fullStop)
		# plotResults(car1, car2)

		car1.downSampleData(currSampleRate)
		car2.downSampleData(currSampleRate)

		accident = Accident([car1, car2], "ParkingLot")
		accident.runAnalysis()
		if car1.analytics.fullStop ==1:
			car1_standstillCount_Low += 1
		if car2.analytics.fullStop ==1:
			car2_standstillCount_Low += 1
		# print("StandStill Car 1: ", car1.analytics.fullStop)
		# print("StandStill Car 2: ", car2.analytics.fullStop)
		# plotResults(car1, car2)

	# print("HighRes Car1 # of stops: ",car1_standstillHighRes)
	car1_HitVector.append((car1_standstillCount_Low*1.0)/car1_standstillCount_High)
	car2_HitVector.append((car2_standstillCount_Low*1.0)/car2_standstillCount_High)
	# print("High: ", car1_standstillCount_High)
	# print("Low: ", car1_standstillCount_Low)
	# print(car1_HitVector)


#Save results to pickle file:
with open('hitRate.pickle', 'wb') as f:
    pickle.dump([sampleRateVector,car1_HitVector,car2_HitVector], f)


# Retrieve the saved expanded training data:
with open('hitRate.pickle','rb') as f:
	sampleRateVector,car1_HitVector,car2_HitVector = pickle.load(f)  


plt.plot(sampleRateVector,car1_HitVector, marker='o' )
plt.plot(sampleRateVector,car2_HitVector, marker='o' )
plt.show()





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


