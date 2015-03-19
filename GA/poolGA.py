'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

13/2/15
'''

import os
from random import randrange as randrange

from MinimisePool import minPool
from MinimiseOff import minOff
from MinimiseMut import minMut
from Select import tournamentSelect as select
from checkPool import checkPool as checkPool

class poolGA:

	def __init__(self,natoms,r_ij
				,eleNums,eleNames
				,eleMasses,mutate
				,n,cross,mutType
				,subString
				,surface
				,surfGA):
		
		self.n = n
		self.r_ij = r_ij
		self.mutate = mutate
		self.natoms = natoms
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.cross = cross
		self.mutType = mutType
		self.subString = subString

		'''
		Surface Object.
		'''

		self.surface = surface
		self.surfGA = surfGA

		''' --- ''' 

		self.stride = natoms + 2

		self.runJobs()

	def runJobs(self):

		notFinished = True

		while notFinished:

			pool = minPool(self.natoms,self.r_ij
				,self.eleNums,self.eleNames
				,self.eleMasses,self.n
				,self.stride,self.subString
				,self.surface,self.surfGA)

			notFinished = self.checkFinished()

		for i in range(self.n,self.n+1000):

			check = checkPool()
			converged = check.Convergence()

			if self.checkRunning():
				
				off = minMut(self.natoms,self.r_ij
					,"random",self.eleNums
					,self.eleNames,self.eleMasses
					,self.n,self.stride
					,self.subString)

			else:
				self.decide()

	def decide(self):

		choice = randrange(0,self.n)

		if choice < self.mutate:

			off = minMut(self.natoms,self.r_ij
				,self.mutType,self.eleNums
				,self.eleNames,self.eleMasses
				,self.n,self.stride
				,self.subString)
		else:

			off = minOff(self.natoms,self.eleNums
				,self.eleNames,self.eleMasses
				,self.n,self.cross,self.stride
				,self.subString)

	def checkRunning(self):

		'''
		Check if pool
		is running.
		'''

		with open("pool.dat","r") as pool:
			for line in pool:
				if "Running" in line:
					return True
				elif "Restart" in line:
					return True

		return False

	def checkFinished(self):

		'''
		Checks if all initial
		geometries relaxed.
		'''

		with open("pool.dat","r") as pool:
			for line in pool:
				if "NotMinimised" in line:
					return True
				elif "Restart" in line:
					return True

		return False
