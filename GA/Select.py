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

--- Selection Class ---

'''

import random as ran

from checkPool import checkPool

class tournamentSelect:

	def __init__(self,n):

		ran.seed()

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

		getEn = checkPool()
		self.energies = getEn.energies

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
		tournament.
		'''

		size=3 
		tournEn=[]

		tourn = ran.sample(range(0,self.n),size)

		for i in tourn:
			tournEn.append(self.energies[i])

		return self.energies.index(min(tournEn))
