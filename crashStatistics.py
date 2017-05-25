from coreEngine import *
from helperFunctions import *
from simulator import *

def countCrashes(numRuns, lookBackMean, lookBackStd):
	crashcounter = 0;

	for x in range(numRuns):
		if x % 10 ==0:
			print(x)
		scene = createAccidentData(lookBackMean, lookBackStd)
		# Create instances of Vehicle:		
		car1 = Vehicle('1C4GJ45331B133332')
		car1.loadData(scene)

		car2 = Vehicle('1J4FT58L2KL609051')
		car2.loadData(scene)

		# create instance of accident with involved vehicles:
		accident = Accident([car1, car2], "ParkingLot")
		# Analyze accident
		accident.runAnalysis()

		# print(car1.analytics.fullStop)
		# print(car2.analytics.fullStop)
		if (car1.analytics.impactTime >0) :
			crashcounter += 1

	# plotResults(car1, car2, scene)
	print("num of crashes: ", crashcounter)
	

################


def assessSamplerate(numRuns, sampleRateVector):

	car1_HitVector = []
	car2_HitVector = []
	car1_AgreementVector = []
	car2_AgreementVector = []
	for currSampleRate in sampleRateVector:
		print("calculating sample rate: ", currSampleRate)
		car1_HitRatio = 0.0
		car2_HitRatio = 0.0

		car1_standstillAgreement =0
		car1_standstillDisAgreement =0
		car2_standstillAgreement =0
		car2_standstillDisAgreement =0

		for x in range(numRuns):
			# create simulated accident data:
			scene = createAccidentData()
			#create vehicles
			car1 = Vehicle('1C4GJ45331B133332')			
			car2 = Vehicle('1J4FT58L2KL609051')
			# Load simulated data into vehicles:
			car1.loadData(scene)
			car2.loadData(scene)

			# create instance of accident with involved vehicles:
			accident = Accident([car1, car2], "ParkingLot")
			# analyze accident
			accident.runAnalysis()

			if car1.analytics.fullStop ==1:
				car1_standstill_High = 1
			else:
				car1_standstill_High = 0

			if car2.analytics.fullStop ==1:
				car2_standstill_High = 1
			else:
				car2_standstill_High = 0


			# downsample the data the vehicles have loaded
			car1.downSampleData(currSampleRate)
			car2.downSampleData(currSampleRate)

			# Create new insance of accident with downsampled data
			accident = Accident([car1, car2], "ParkingLot")
			# analyze accident with downsampled data:
			accident.runAnalysis()

			if car1.analytics.fullStop ==1:
				car1_standstill_Low = 1
			else:
				car1_standstill_Low = 0

			if car2.analytics.fullStop ==1:
				car2_standstill_Low = 1
			else:
				car2_standstill_Low = 0


			if car1_standstill_High == 1:
				if car1_standstill_Low == 1:
					car1_standstillAgreement +=1
				else:
					car1_standstillDisAgreement +=1

			if car2_standstill_High == 1:
				if car2_standstill_Low == 1:
					car2_standstillAgreement +=1
				else:
					car2_standstillDisAgreement +=1

		
		car1_agreementRatio = (car1_standstillAgreement*1.0)/(car1_standstillAgreement+car1_standstillDisAgreement)
		car2_agreementRatio = (car2_standstillAgreement*1.0)/(car2_standstillAgreement+car2_standstillDisAgreement)

		car1_AgreementVector.append(car1_agreementRatio)
		car2_AgreementVector.append(car2_agreementRatio)

	#Save results to pickle file:
	with open('hitRate.pickle', 'wb') as f:
	    pickle.dump([sampleRateVector, car1_AgreementVector, car2_AgreementVector], f)

	# Retrieve the saved expanded training data:
	with open('hitRate.pickle','rb') as f:
		sampleRateVector,car1_AgreementVector, car2_AgreementVector = pickle.load(f) 

	print(car1_AgreementVector)
	print(car2_AgreementVector)

	plt.plot(sampleRateVector,car1_AgreementVector, marker='o' )
	plt.plot(sampleRateVector,car2_AgreementVector, marker='o' )
	plt.show()



def assessLookBackRate(numRuns, sampleRate):
	lookBackMeanVector =[0.5,1,1.5,2,2.5,3,3.5,4]

	lookBackStd = 2.5

	car1_HitVector = []
	car2_HitVector = []
	car1_AgreementVector = []
	car2_AgreementVector = []

	for lookBackMean in lookBackMeanVector:
		
		print("calculating lookback mean: ", lookBackMean)
		car1_HitRatio = 0.0
		car2_HitRatio = 0.0

		car1_standstillAgreement =0
		car1_standstillDisAgreement =0
		car2_standstillAgreement =0
		car2_standstillDisAgreement =0

		for x in range(numRuns):
			# create simulated accident data:
			scene = createAccidentData(lookBackMean, lookBackStd)
			#create vehicles
			car1 = Vehicle('1C4GJ45331B133332')			
			car2 = Vehicle('1J4FT58L2KL609051')
			# Load simulated data into vehicles:
			car1.loadData(scene)
			car2.loadData(scene)

			# create instance of accident with involved vehicles:
			accident = Accident([car1, car2], "ParkingLot")
			# analyze accident
			accident.runAnalysis()

			if car1.analytics.fullStop ==1:
				car1_standstill_High = 1
			else:
				car1_standstill_High = 0

			if car2.analytics.fullStop ==1:
				car2_standstill_High = 1
			else:
				car2_standstill_High = 0


			# downsample the data the vehicles have loaded
			car1.downSampleData(sampleRate)
			car2.downSampleData(sampleRate)

			# Create new insance of accident with downsampled data
			accident = Accident([car1, car2], "ParkingLot")
			# analyze accident with downsampled data:
			accident.runAnalysis()

			if car1.analytics.fullStop ==1:
				car1_standstill_Low = 1
			else:
				car1_standstill_Low = 0

			if car2.analytics.fullStop ==1:
				car2_standstill_Low = 1
			else:
				car2_standstill_Low = 0


			if car1_standstill_High == 1:
				if car1_standstill_Low == 1:
					car1_standstillAgreement +=1
				else:
					car1_standstillDisAgreement +=1

			if car2_standstill_High == 1:
				if car2_standstill_Low == 1:
					car2_standstillAgreement +=1
				else:
					car2_standstillDisAgreement +=1

			
		car1_agreementRatio = (car1_standstillAgreement*1.0)/(car1_standstillAgreement+car1_standstillDisAgreement)
		car2_agreementRatio = (car2_standstillAgreement*1.0)/(car2_standstillAgreement+car2_standstillDisAgreement)

		car1_AgreementVector.append(car1_agreementRatio)
		car2_AgreementVector.append(car2_agreementRatio)

	#Save results to pickle file:
	with open('hitRate.pickle', 'wb') as f:
	    pickle.dump([lookBackMeanVector, car1_AgreementVector, car2_AgreementVector], f)

	# Retrieve the saved expanded training data:
	with open('hitRate.pickle','rb') as f:
		lookBackMeanVector,car1_AgreementVector, car2_AgreementVector = pickle.load(f) 

	print(car1_AgreementVector)
	print(car2_AgreementVector)

	plt.plot(lookBackMeanVector,car1_AgreementVector, marker='o' )
	plt.plot(lookBackMeanVector,car2_AgreementVector, marker='o' )
	plt.show()

countCrashes(100, 1.5, 2.5)

# numRuns = 100
# sampleRateVector = [100,50,10,5,2,1,0.5,0.1]
# assessSamplerate(numRuns, sampleRateVector)


# numRuns = 3000
# sampleRate = 1
# assessLookBackRate(numRuns, sampleRate)







