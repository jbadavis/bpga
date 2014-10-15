'''
Selection

Jack Davis

13/10/14
'''

from random import randrange

class tournamentSelect:

	def __init__(self,n):

		self.select(n)

	def select(self,n):

		'''
		Selects random 
		pair from pool
		for crossover
		'''

		clust1 = randrange(1,n+1)
		clust2 = randrange(1,n+1)

		while clust2 == clust1:
			clust2 = randrange(1,n)

		self.pair = [clust1,clust2]