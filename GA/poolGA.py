'''
poolGA

Jack Davis

10/10/14
'''

import os
from random import randrange as randrange

from MinimisePool import minPool
from MinimiseOff import minOff
from MinimiseMut import minMut
from Select import tournamentSelect as select
from checkPool import checkPool as checkPool

class poolGA:

	def __init__(self,natoms,eleNums,eleNames,eleMasses,mutate,n,hpc,mpitasks):
		
		self.n = n
		self.mutate = mutate
		self.natoms = natoms
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.mpitasks = mpitasks
		self.stride = natoms + 2
		self.hpc = hpc

		self.runJobs()

	def runJobs(self):

		notFinished = True

		while notFinished:

			pool = minPool(self.natoms,self.eleNums,self.eleNames,
				self.eleMasses,self.n,self.stride,self.hpc,self.mpitasks)

			notFinished = self.checkFinished()

		for i in range(self.n,self.n+1000):

			check = checkPool()
			converged = check.Convergence()

			self.decide()

	def decide(self):

		choice = randrange(0,self.n)

		if choice < self.mutate:
			off = minMut(self.natoms,self.eleNums,self.eleNames,self.eleMasses
						,self.n,self.stride,self.hpc,self.mpitasks)
		else:
			off = minOff(self.natoms,self.eleNums,self.eleNames,self.eleMasses
						,self.n,self.stride,self.hpc,self.mpitasks)

	def checkFinished(self):

		'''
		Checks if all initial
		geometries relaxed.
		'''

		with open("pool.dat","r") as pool:
			for line in pool:
				if "NotMinimised" in line:
					return True

		return False

	# def checkRunning(self):

	# 	with open("pool.dat","r") as pool:
	# 		for line in pool:
	# 			if "Running" in line:
	# 				return True

	# 	return False
