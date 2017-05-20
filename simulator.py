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
		self.datalog.speed = []
		self.datalog.time = []
		self.datalog.dist = []
		self.datalog.parkdist = []		
		
	def assignBehavior(self):
		self.startTime = random.uniform(0.5, 1.5)
		self.acceleration = random.uniform(0.4, 1.2)
		self.vmax = random.uniform(0.7, 1.5)
		self.brakeInitDist = random.uniform(2, 10)
		self.deceleration = random.uniform(-0.7, -1.5)
		self.maxParkSensorDist = random.uniform(2.5,3.5)

	def conductManeuverStep(self,scene):
		if scene.currTime < self.startTime:
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
		self.datalog.speed.append(self.speed)
		self.datalog.dist.append(self.distTraveled)

		self.datalog.time.append(scene.currTime)
		if scene.distance > self.maxParkSensorDist:
			self.datalog.parkdist.append(math.inf)
		else:
			self.datalog.parkdist.append(scene.distance)


class Scene(object):
	def __init__(self):
		self.accidentType = 1
		self.aisleWidth = 10
		self.endTime = 10
		self.distance = self.aisleWidth
		self.datalog = Data()
		self.datalog.dist = []
		self.datalog.time = []
		self.stepSize = 0.01
		self.crashOccurred = False
		self.currTime = 0
		
def simulate(scene, vehicle1, vehicle2):
	# timeVector = []

	if scene.accidentType == 1: # both back up		
		
		while scene.currTime < scene.endTime:

			vehicle1.conductManeuverStep(scene)
			vehicle2.conductManeuverStep(scene)

			scene.distance = scene.aisleWidth - vehicle1.distTraveled - vehicle2.distTraveled
			scene.datalog.dist.append(scene.distance)
			scene.datalog.time.append(scene.currTime)

			vehicle1.logEventData(scene)
			vehicle2.logEventData(scene)
			
			if scene.distance <=0:
				scene.crashOccurred = True
				break
			elif (vehicle1.speed ==0) and (vehicle2.speed==0) and (scene.currTime > vehicle1.startTime) and (scene.currTime > vehicle2.startTime):
				break

			scene.currTime = scene.currTime + scene.stepSize


def createAccidentData():
	# initialize scene and vehicles:
	scene1 = Scene()
	car1 = Vehicle()
	car1.assignBehavior()
	car2 = Vehicle()
	car2.assignBehavior()

	# Run simulation:
	simulate(scene1, car1, car2)
	return car1.datalog, car2.datalog


car1Data, car2Data = createAccidentData()

car2dist = np.array(car2Data.dist)
plt.plot(car1Data.time, car1Data.dist)
plt.plot(car2Data.time, 10-car2dist)
plt.show()









