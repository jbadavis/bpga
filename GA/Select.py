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

		# If running flag found choose new cluster.
		while self.checkRunning():
			pos = self.tournEnergy.index("Running")
			random = randrange(0,self.n)
			tournList[pos] = random
			self.tournEnergy[pos] = self.energies[random]

		# Get index of lowest energy from tournament. 
		lowest = self.tournEnergy.index(min(self.tournEnergy))

		return tournList[lowest]

	def checkRunning(self):

		for i in range(2):
			if self.tournEnergy[i] == "Running":
				return True