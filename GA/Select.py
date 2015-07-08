'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

10/10/14

--- Roulette Wheel Selection Class ---

'''

import random as ran
import numpy as np

from checkPool import checkPool

class select:

	def __init__(self,nPool):

		ran.seed()

		self.nPool = nPool
		self.getFitness()

		# self.getEnergies()
		# self.selectClusters(n)

	def getFitness(self):

		self.fitness = []
		self.energies = sorted(checkPool().energies)

		energyRange = self.energies[len(self.energies)-1] - self.energies[0]

		for energy in self.energies:
			fit = 0.5*(1-np.tanh(2.*((energy-self.energies[0])/energyRange)-1.))
			self.fitness.append(fit)

	def roulette(self):

		self.pair = []

		while len(self.pair) < 2:

			ranPos = ran.randrange(0,self.nPool)
			ranFit = ran.uniform(0,1)

			if ranFit < self.fitness[ranPos] and ranPos not in self.pair:
				self.pair.append(ranPos)

		return self.pair

	# def selectClusters(self,n):

	# 	'''
	# 	Selects random 
	# 	pair from pool
	# 	for crossover.
	# 	'''

	# 	clust1 = self.tournament()
	# 	clust2 = self.tournament()

	# 	while clust2 == clust1:
	# 		clust2 = self.tournament()

	# 	self.pair = [clust1,clust2]

	# def tournament(self):

	# 	'''
	# 	Randomly select 
	# 	tournament.
	# 	'''

	# 	size = 4
	# 	tournEn = []

	# 	tourn = ran.sample(range(0,self.nPool),size)

	# 	for i in tourn:
	# 		tournEn.append(self.energies[i])

	# 	return self.energies.index(min(tournEn))
