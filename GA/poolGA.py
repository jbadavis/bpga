'''
poolGA

Jack Davis

10/10/14
'''

import os

from MinimisePool import minPool
from MinimiseOff import minOff
from Select import tournamentSelect as select
from checkPool import checkPool as checkPool

class poolGA:

	def __init__(self,natoms,eleNums,eleNames,eleMasses,n,hpc,mpitasks):
		
		self.n = n
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
		Running = True

		while notFinished:

			pool = minPool(self.natoms,self.eleNums,self.eleNames,
				self.eleMasses,self.n,self.stride,self.hpc,self.mpitasks)

			notFinished = self.checkFinished()

		# while Running:
		# 	Running = self.checkRunning()
		# 	pass

		for i in range(self.n,self.n+1000):

			check = checkPool()
			converged = check.Convergence()

			off = minOff(self.natoms,self.eleNames,self.eleMasses
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

	def checkRunning(self):

		with open("pool.dat","r") as pool:
			for line in pool:
				if "Running" in line:
					return True

		return False
