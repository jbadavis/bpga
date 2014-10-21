'''
Minimiser

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

		for i in range(self.n):

			pool = minPool(self.natoms,self.eleNums,self.eleNames,
				self.eleMasses,self.n,self.stride,self.hpc,self.mpitasks)

		while self.checkFinished() == False:
			pass
		
		for i in range(self.n,self.n+1000):

			calcNum = self.findLastDir() + 1

			check = checkPool()
			converged = check.Convergence()

			off = minOff(calcNum,self.natoms,self.eleNames,self.eleMasses
				,self.n,self.stride,self.hpc,self.mpitasks)

	def findPair(self):

		'''
		From tournamentSelect the
		exact positions of the 
		random clusters is found in 
		the pool.
		'''

		# Select random pair 
		selectPair = select(self.n)
		pair = selectPair.pair

		#Postions of pair in poollist
		c1 = ((pair[0]-1)*self.stride)
		c2 = ((pair[1]-1)*self.stride)

		self.readPool()

		self.clus1 = self.poolList[c1+2:c1+self.stride]
		self.clus2 = self.poolList[c2+2:c2+self.stride]

		self.poolPos = [c1,c2]

	def checkFinished(self):

		'''
		Checks if all initial
		geometries relaxed.
		'''

		with open("pool.dat","r") as pool:
			for line in pool:
				if "Running" in line:
					return False

		return True

	def findLastDir(self):

		'''
		Finds directory
		containing last
		calculation.
		'''

		calcList = []
		dirList = os.listdir(".")

		for i in dirList:
			try:
				calcList.append(int(i))
			except ValueError:
				continue

		calcList = sorted(calcList)

		lastCalc = calcList[len(calcList)-1]

		return lastCalc
