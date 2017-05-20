import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random
import math


class Data:
	pass

class Vehicle(object):
	def __init__(self):
		self.name = self
		self.speed = 0
		self.distTraveled = 0
		self.datalog = Data()
		self.datalog.speed = np.empty([1])
		self.datalog.time = np.empty([1])
		self.datalog.dist = np.empty([1])
		self.datalog.parkdist = np.empty([1])
		
	def assignBehavior(self):
		self.startTime = random.uniform(0.5, 1.5)
		self.acceleration = random.uniform(0.4, 1.2)
		self.vmax = random.uniform(0.7, 1.5)
		self.brakeInitDist = random.uniform(2, 10)
		self.deceleration = random.uniform(-0.7, -1.5)
		self.maxParkSensorDist = random.uniform(2.5,3.5)

	def conductManeuverStep(self,scene):
		if scene.currTime < self.startTime or scene.crashOccurred:
			ax = 0
		else:
			if self.distTraveled < self.brakeInitDist:
				ax = self.acceleration
			else: 
				ax = self.deceleration
		self.speed = min(self.speed + ax*scene.stepSize, self.vmax )
		self.speed = max(self.speed + ax*scene.stepSize, 0)
		self.distTraveled = self.distTraveled+self.speed*scene.stepSize

	def logEventData(self, scene):
		self.datalog.speed = np.append(self.datalog.speed, self.speed)		
		self.datalog.dist = np.append(self.datalog.dist, self.distTraveled)

		self.datalog.time = np.append(self.datalog.time, scene.currTime)
		if scene.distance > self.maxParkSensorDist:
			self.datalog.parkdist = np.append(self.datalog.parkdist,math.inf)
		else:
			self.datalog.parkdist = np.append(self.datalog.parkdist, scene.distance)


class Scene(object):
	def __init__(self, accidentType):
		self.accidentType = "ParkingLot"
		self.aisleWidth = 10
		self.endTime = 10
		self.distance = self.aisleWidth
		self.datalog = Data()
		self.datalog.dist = np.empty([1])
		self.datalog.time = np.empty([1])
		self.stepSize = 0.01
		self.crashOccurred = False
		self.currTime = 0
		self.postCrashRelevantSpan = 3
		self.postCrashTime = 0
		
def simulate(scene, vehicle1, vehicle2):
	# timeVector = []

	if scene.accidentType == "ParkingLot": # both back up		
		
		while scene.currTime < scene.endTime:

			vehicle1.conductManeuverStep(scene)
			vehicle2.conductManeuverStep(scene)

			scene.distance = scene.aisleWidth - vehicle1.distTraveled - vehicle2.distTraveled
			scene.datalog.dist = np.append(scene.datalog.dist, scene.distance)
			scene.datalog.time = np.append(scene.datalog.time, scene.currTime)

			vehicle1.logEventData(scene)
			vehicle2.logEventData(scene)
			
			if scene.distance <=0:
				scene.crashOccurred = True
				vehicle1.speed =0
				vehicle2.speed = 0
				scene.postCrashTime = scene.postCrashTime + scene.stepSize
				if scene.postCrashTime > scene.postCrashRelevantSpan:
					break
			elif (vehicle1.speed ==0) and (vehicle2.speed==0) and (scene.currTime > vehicle1.startTime) and (scene.currTime > vehicle2.startTime) and (scene.crashOccurred==False):
				break

			scene.currTime = scene.currTime + scene.stepSize


def createAccidentData():
	# initialize scene and vehicles:
	scene1 = Scene("ParkingLot")
	car1 = Vehicle()
	car1.assignBehavior()
	car2 = Vehicle()
	car2.assignBehavior()

	# Run simulation:
	simulate(scene1, car1, car2)
	return car1.datalog, car2.datalog


car1Data, car2Data = createAccidentData()

plt.plot(car1Data.time, car1Data.dist)
plt.plot(car2Data.time, 10-car2Data.dist)
plt.show()









