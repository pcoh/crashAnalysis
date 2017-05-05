import os
import os.path
import csv
import numpy
from numpy import genfromtxt


# define empty class for data structure:
class Data:
	pass

# define vechicle class:
class Vehicle(object):

	def __init__(self, VIN):
		self.VIN = VIN
		self.data = Data()
		
		self.make = 'unknown'
		self.model = 'unknown'
	
	def loadData(self):
		fileName = os.getcwd() + '/'+ self.VIN + '.csv'
		if (os.path.isfile(fileName)):
			self.data.raw = genfromtxt(fileName, delimiter=',')
			self.data.time = self.data.raw[1:,0]
			self.data.speedometer = self.data.raw[1:,0]
		else:
			print("No data available for ", VIN )

# define accident class:
class Accident(object):

	def __init__(self, VINList, category):
		self.category = category
		self.involvedVehicles = VINList

	def runAnalysis(self):
		if(self.category == "ParkingLot"):
			print("running analysis")
			# establishImpactTime()
		else:
			print("unable to analyse this type of accident")

	# def establishImpactTime():
		if(parking distance sensor signal is available):
			find time at which the indicated distance of the first sensor becomes (very close to) zero.
		elif (RELEVANT impact acceleromer data is available):
			find time at which accel from impact sensor starts to diverge from accel of vehicle.
		elif (brakeOn/Off signal is available)
			find time at which deceleration becomes greater that possible from coast-down
			(need to consider gradient of road??)
		else:
			if(mid to high speed impact): 
				find time at which abs(acel_X) becomes greater than what could be achieved by braking.
			else:
				??????????




# Create instances of Vehicle:		
car1 = Vehicle('1C4GJ45331B133332')
car1.loadData()

car2 = Vehicle('1J4FT58L2KL609051')
car2.loadData()


# create instance of accident with involved vehicles:
accident = Accident([car1, car2], "ParkingLot")


for parties in accident.involvedVehicles:
	print(parties.VIN)
	print(parties.data.time)


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


