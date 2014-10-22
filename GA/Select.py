'''
Selection

Jack Davis

13/10/14
'''

from random import randrange

class tournamentSelect:

	def __init__(self,n):

		self.n = n
		self.energies = []
		self.getEnergies()
		self.selectClusters(n)

	def getEnergies(self):

		'''
		Get final energies
		from pool.dat after
		convergence.
		'''

		with open("pool.dat","r") as pool:
			for line in pool:
				if "Finished Energy" in line:
					energyList = line.split()
					self.energies.append(float(energyList[3]))
				if "Running" in line:
					self.energies.append(100.0)

	def selectClusters(self,n):

		'''
		Selects random 
		pair from pool
		for crossover
		'''

		clust1 = self.tournament()
		clust2 = self.tournament()

		while clust2 == clust1:
			clust2 = self.tournament()

		self.pair = [clust1,clust2]

	def tournament(self):

		'''
		Selects random 
		clusters, chooses
		the one with the 
		lowest energy.
		'''

		# Change to accept larger tournaments
		size = 2 # Do not change!
		tournList = []

		# Select two random clusters for comparison.
		for i in range(size):
			tournList.append(randrange(1,self.n+1))

		# Ensure that the two clusters are different. 
		while tournList[0] == tournList[1]:
			tournList[1] = randrange(1,self.n+1)

		# Get energies of two chosen clusters.
		self.tournEnergy = []
		for i in tournList:
			self.tournEnergy.append(self.energies[i-1])

		# Get index of lowest energy from tournament. 
		lowest = self.tournEnergy.index(min(self.tournEnergy))

		return tournList[lowest]

	# def checkRunning(self):

	# 	for i in range(len(self.tournEnergy)):
	# 		if self.tournEnergy[i] == "Running":
	# 			print "Running"
	# 			return True
	# 			break

	# 	return False