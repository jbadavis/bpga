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
		self.select(n)

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

	def select(self,n):

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
		tournament = []

		for i in range(size):
			tournament.append(randrange(1,self.n+1))

		while tournament[0] == tournament[1]:
			tournament[1] = randrange(1,self.n+1)

		tournEnergy = []

		for i in tournament:
			tournEnergy.append(self.energies[i-1])

		lowest = tournEnergy.index(min(tournEnergy))

		return tournament[lowest]
