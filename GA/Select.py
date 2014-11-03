'''
Selection

Jack Davis

13/10/14
'''

from random import randrange
import random as ran

class tournamentSelect:

	def __init__(self,n):

		self.n = n
		self.energies = []
		self.getEnergies()
		self.selectClusters(n)
		ran.seed()

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
					self.energies.append("Running")

	def selectClusters(self,n):

		'''
		Selects random 
		pair from pool
		for crossover.
		'''

		clust1 = self.tournament()
		clust2 = self.tournament()

		while clust2 == clust1:
			clust2 = self.tournament()

		self.pair = [clust1,clust2]

	def tournament(self):

		'''
		Randomly select 
		tournament ensuring 
		a running calculation
		isn't chosen.
		'''

		size=2 
		self.tournList=[]
		tournEnergy=[]

		for i in range(size):
			self.tournList.append(randrange(0,self.n))

		while self.tournList[0] == self.tournList[1]:
			self.tournList[1] = randrange(0,self.n)

		while self.checkRunning():
			self.tournList[self.index] = randrange(self.n)

		for i in range(size):
			tournEnergy.append(self.energies[self.tournList[i]])

		return self.energies.index(min(tournEnergy))

	def checkRunning(self):

		for i in range(2):
			self.index = self.tournList[i]
			if self.energies[self.index] == "Running":
				self.index = i
				return True
				break
		return False

	# def tournament(self):

	# 	'''
	# 	Selects random 
	# 	clusters, chooses
	# 	the one with the 
	# 	lowest energy.
	# 	'''

	# 	# Change to accept larger tournaments
	# 	size = 2 # Do not change!
	# 	tournList = []

	# 	# Select two random clusters for comparison.
	# 	for i in range(size):
	# 		tournList.append(randrange(0,self.n))

	# 	# Ensure that the two clusters are different. 
	# 	while tournList[0] == tournList[1]:
	# 		tournList[1] = randrange(0,self.n)

	# 	# Get energies of two chosen clusters.
	# 	self.tournEnergy = []
	# 	for i in tournList:
	# 		self.tournEnergy.append(self.energies[i-1])

	# 	# If running flag found choose new cluster.
	# 	while self.checkRunning():
	# 		pos = self.tournEnergy.index("Running")
	# 		random = randrange(0,self.n)
	# 		tournList[pos] = random
	# 		self.tournEnergy[pos] = self.energies[random]

	# 	self.tournEnergy = [-107.40002552, -106.60122626]

	# 	# Get index of lowest energy from tournament. 
	# 	lowest = self.tournEnergy.index(min(self.tournEnergy))

	# 	print tournList
	# 	print tournList[lowest]

	# 	return tournList[lowest]

	# def checkRunning(self):

	# 	for struc in self.tournEnergy:
	# 		if struc == "Running":
	# 			return True
	# 			break
	# 	return False 
	# 		# if self.tournEnergy[i] == "Running":
	# 		# 	return True
	# 		# 	break
	# 		# return False