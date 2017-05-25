import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random
import math

class Data:
	pass

class SimVehicle(object):
	def __init__(self, VIN):
		self.name = self
		self.VIN = VIN
		self.speed = 0
		self.ax = 0
		self.distTraveled = 0
		self.currPerceivedSpace = math.inf
		self.timeSinceLookBack = 0
		self.recognizedDanger = 0


		self.datalog = Data()
		self.datalog.time = np.zeros([1])
		self.datalog.speed = np.zeros([1])		
		self.datalog.dist = np.zeros([1])
		self.datalog.parkdist_rear = np.zeros([1])
		self.datalog.accel_x = np.zeros(1)
		self.datalog.brakeOn = np.zeros(1)
		self.driverlog = Data()
		self.driverlog.perceivedSpace = np.zeros(1)
		
	def assignBehavior(self, lookBackMean = 1.5, lookBackStd = 2.5):
		self.startTime = random.uniform(0.5, 1.0)
		self.acceleration = random.gauss(0.6, 0.25)

		self.vmax = random.gauss(1.1, 0.2)
		self.deceleration = min(0,random.gauss(-1.1, 0.2))
		self.maxParkSensorDist = 2.5
		self.lookBackInterval = max(0.3, random.gauss(lookBackMean, lookBackStd))

	def checkForDanger(self, scene):
		if (scene.currTime >= self.startTime -0.2) and (scene.currTime <= self.startTime -0.15): # Driver looks back just before starting to back out
			self.timeSinceLookBack = math.inf

		if self.timeSinceLookBack >= self.lookBackInterval: # Driver looks back at given intervals
			self.timeSinceLookBack = 0
			self.currPerceivedSpace = scene.distance
			if scene.distance < (scene.aisleWidth - self.distTraveled -0.3) or scene.distance < 1.5: #only recognized that other car moved if other car moved more than 0.3m but also stops if distance from other car is less than 1.5m)
				self.recognizedDanger = 1
		self.timeSinceLookBack += scene.stepSize


	def conductManeuverStep(self,scene):
		if scene.currTime < self.startTime or scene.crashOccurred:
			self.ax = 0
		else:
			if self.recognizedDanger == 1:
				self.ax = self.deceleration
			else:
				self.ax = self.acceleration

		self.speed = min(self.speed + self.ax*scene.stepSize, self.vmax )
		self.speed = max(self.speed + self.ax*scene.stepSize, 0)
		self.distTraveled = self.distTraveled+self.speed*scene.stepSize

	def logEventData(self, scene):
		self.datalog.speed = np.append(self.datalog.speed, self.speed)		
		self.datalog.dist = np.append(self.datalog.dist, self.distTraveled)
		if len(self.datalog.dist)>1:
			self.datalog.accel_x = np.append(self.datalog.accel_x,(self.datalog.speed[-1] - self.datalog.speed[-2])/scene.stepSize)
		else:
			self.datalog.accel_x = np.append(self.datalog.accel_x, 0)

		self.datalog.time = np.append(self.datalog.time, scene.currTime)
		if scene.distance > self.maxParkSensorDist:
			self.datalog.parkdist_rear = np.append(self.datalog.parkdist_rear,math.inf)
		else:
			self.datalog.parkdist_rear = np.append(self.datalog.parkdist_rear, scene.distance)

		if self.ax >= 0:
			self.datalog.brakeOn = np.append(self.datalog.brakeOn, 0)
		else:
			self.datalog.brakeOn = np.append(self.datalog.brakeOn, 1)

		self.driverlog.perceivedSpace =np.append(self.driverlog.perceivedSpace, self.currPerceivedSpace )


	def cleanLog(self):
		self.datalog.time = np.delete(self.datalog.time, 0)
		self.datalog.speed = np.delete(self.datalog.speed, 0)
		self.datalog.dist = np.delete(self.datalog.dist, 0)
		self.datalog.parkdist_rear = np.delete(self.datalog.parkdist_rear, 0)
		self.datalog.accel_x =  np.delete(self.datalog.accel_x, 0)
		self.datalog.brakeOn =  np.delete(self.datalog.brakeOn, 0)
		self.driverlog.perceivedSpace =  np.delete(self.driverlog.perceivedSpace, 0)


class Scene(object):
	def __init__(self, accidentType, involvedCars):
		self.accidentType = 'ParkingLot'
		self.involvedCars =involvedCars
		self.aisleWidth = 7.8
		self.endTime = 10
		self.distance = self.aisleWidth
		self.datalog = Data()
		self.datalog.dist = np.zeros([1])
		self.datalog.time = np.zeros([1])
		self.stepSize = 0.01
		self.crashOccurred = False
		self.currTime = 0
		self.postCrashRelevantSpan = 3
		self.postCrashTime = 0

		
	def simulate(self, vehicle1, vehicle2):
		# print("Simulating") 

		if self.accidentType == 'ParkingLot': # both back up		
			
			while self.currTime < self.endTime:
				vehicle1.checkForDanger(self)
				vehicle2.checkForDanger(self)
				# print("v2 time since look: ", vehicle2.timeSinceLookBack)

				vehicle1.conductManeuverStep(self)
				vehicle2.conductManeuverStep(self)

				self.distance = self.aisleWidth - vehicle1.distTraveled - vehicle2.distTraveled
				self.datalog.dist = np.append(self.datalog.dist, self.distance)
				self.datalog.time = np.append(self.datalog.time, self.currTime)

				vehicle1.logEventData(self)
				vehicle2.logEventData(self)
				
				if self.distance <=0:
					self.crashOccurred = True
					vehicle1.speed =0
					vehicle2.speed = 0
					self.postCrashTime = self.postCrashTime + self.stepSize
					if self.postCrashTime > self.postCrashRelevantSpan:
						break

				elif (vehicle1.speed ==0) and (vehicle2.speed==0) and (self.currTime > vehicle1.startTime) and (self.currTime > vehicle2.startTime) and (self.crashOccurred==False):
					break

				self.currTime = self.currTime + self.stepSize

			vehicle1.cleanLog()
			vehicle2.cleanLog()
			self.cleanLog()

	def cleanLog(self):
		self.datalog.time = np.delete(self.datalog.time, 0)
		self.datalog.dist = np.delete(self.datalog.dist, 0)



def createAccidentData(lookBackMean=1.5, lookBackStd=2.5):
	# initialize scene and vehicles:
	
	car1 = SimVehicle('1C4GJ45331B133332')
	car1.assignBehavior(lookBackMean, lookBackStd)
	car2 = SimVehicle('1J4FT58L2KL609051')
	car2.assignBehavior(lookBackMean, lookBackStd)
	# print("Car 1 Lookback interval: ", car1.lookBackInterval)
	# print("Car 2 Lookback interval: ", car2.lookBackInterval)
	scene = Scene('ParkingLot', [car1, car2])

	# Run simulation:
	scene.simulate( car1, car2)

	return scene







