import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random




class Data:
	pass

class Vehicle(object):
	def __init__(self):
		self.name = self
		self.speed = 0
		self.distTraveled = 0
		self.datalog = Data()
		self.datalog.speed = []
		self.datalog.dist = []
		# self.VIN = VIN
		# self.data = Data()
		
		# self.make = 'unknown'
		# self.model = 'unknown'
		
	def assignBehavior(self):
		self.startTime = random.uniform(0.5, 1.5)
		self.acceleration = random.uniform(0.4, 1.2)
		self.vmax = random.uniform(0.7, 1.5)
		self.brakeInitDist = random.uniform(2, 10)
		self.deceleration = random.uniform(-0.7, -1.5)

	def conductManeuverStep(self,scene,currTime):
		if currTime < self.startTime:
			ax = 0
		else:
			if self.distTraveled < self.brakeInitDist:
				ax = self.acceleration
			else: 
				ax = self.deceleration
		self.speed = min(self.speed + ax*scene.stepSize, self.vmax )
		self.speed = max(self.speed + ax*scene.stepSize, 0)
		self.distTraveled = self.distTraveled+self.speed*scene.stepSize


class Scene(object):
	def __init__(self):
		self.accidentType = 1
		self.aisleWidth = 10
		self.endTime = 10
		self.datalog = Data()
		self.datalog.dist = []
		self.stepSize = 0.01
		self.crashOccurred = False
		
def simulate(scene, vehicle1, vehicle2):
	timeVector = []
	vehicle1.datalog.speed = []
	vehicle1.datalog.dist = []
	

	if scene.accidentType == 1: # both back up
		currTime = 0
		
		while currTime < scene.endTime:

			vehicle1.conductManeuverStep(scene, currTime)
			vehicle2.conductManeuverStep(scene, currTime)
			
			vehicle1.datalog.speed.append(vehicle1.speed)
			vehicle1.datalog.dist.append(vehicle1.distTraveled)
			vehicle2.datalog.speed.append(vehicle2.speed)
			vehicle2.datalog.dist.append(vehicle2.distTraveled)

			distance = scene.aisleWidth - vehicle1.distTraveled - vehicle2.distTraveled
			scene.datalog.dist.append(distance)
			timeVector.append(currTime)
			
			if distance <=0:
				scene.crashOccurred = True
				break
			elif (vehicle1.speed ==0) and (vehicle2.speed==0) and (currTime > car1.startTime) and (currTime > car2.startTime):
				break

			currTime = currTime + scene.stepSize
		

# initialize scene and vehicles:
scene1 = Scene()
car1 = Vehicle()
car1.assignBehavior()
car2 = Vehicle()
car2.assignBehavior()

# Run simulation:
simulate(scene1, car1, car2)


#Plot results:
car2dist = np.array(car2.datalog.dist)
plt.plot(car1.datalog.dist)
plt.plot(10-car2dist)
plt.show()

# plt.plot(car1.datalog.speed)
# plt.show()
# plt.plot(scene1.datalog.dist)
# plt.show()







