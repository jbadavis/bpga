'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

20/3/15

--- BPGA Input file ---

'''

import os,sys
from random import randrange, uniform

from MinimiseRan import minRan 
from MinimiseOff import minOff
from MinimiseMut import minMut
from checkPool import checkPool as checkPool

class poolGA:

	def __init__(self,natoms,r_ij
				,eleNums,eleNames
				,eleMasses,mutate
				,nPool,cross,mutType
				,subString
				,boxAdd
				,surface
				,surfGA):

		self.nPool = nPool
		self.r_ij = r_ij
		self.mutate = mutate
		self.natoms = natoms
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.cross = cross
		self.mutType = mutType
		self.subString = subString
		self.boxAdd = boxAdd

		'''
		Surface Object.
		'''

		self.surface = surface
		self.surfGA = surfGA

		''' --- ''' 

		self.stride = natoms + 2

		self.run()

	def run(self):

		'''
		Minimise random geometries and
		add them to the pool.dat file.
		'''

		while self.getPoolSize() < self.nPool:

			pool = minRan(self.natoms,self.r_ij
						,self.eleNums,self.eleNames
						,self.eleMasses,self.nPool
						,self.stride,self.subString
						,self.boxAdd
						,self.surface,self.surfGA)

		sys.exit()

		'''
		Once nPool structure are in
		pool.dat begin crossover
		and mutation. 
		'''
			
		'''
		Set the mutation rate.
		'''

		mutateRate = self.mutate * self.nPool

		for i in range(1000): 

			choice = uniform(0,self.nPool)

			if choice < mutateRate:

				off = minMut(self.natoms,self.r_ij
					,self.mutType,self.eleNums
					,self.eleNames,self.eleMasses
					,self.nPool,self.stride
					,self.subString,self.boxAdd
					,self.surface,self.surfGA)
			else:

				off = minOff(self.natoms,self.eleNums
					,self.eleNames,self.eleMasses
					,self.nPool,self.cross,self.stride
					,self.subString,self.boxAdd
					,self.surface,self.surfGA)

	def getPoolSize(self):

		if os.path.exists("pool.dat") == False:
			return 0
		else: 
			with open("pool.dat","r") as pool:
				poolList = pool.readlines()
				poolSize = len(poolList) / (self.natoms + 2)
				return poolSize 

