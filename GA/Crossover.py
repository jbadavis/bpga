'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

20/3/15

--- Cut and Splice Class ---

'''

import numpy as np
import random as ran

import Database as db

from Select import tournamentSelect as select
from checkPool import checkPool
from CoM import CoM 

import sys

class crossover:

	def __init__(self,crossType,nPool
				,stride,eleNums
				,eleNames,natoms):

		self.crossType = crossType

		self.nPool = nPool
		self.stride = stride
		self.eleNames = eleNames
		self.eleNums = eleNums
		self.natoms = natoms 

		'''
		During initialisation the 
		clusters are selected and 
		then rotated and sorted. 
		'''
		self.findPair()
		self.prepare()

	def findPair(self):

		'''
		Using the roulette method select the
		exact positions of the 
		random clusters from the pool
		'''

		self.pairPos = select(self.nPool).roulette()

		#Postions of pair in poollist
		c1 = self.pairPos[0] * self.stride
		c2 = self.pairPos[1] * self.stride

		poolList = db.readPool()

		self.clus1 = poolList[c1+2:c1+self.stride]
		self.clus2 = poolList[c2+2:c2+self.stride]

		self.pair = [self.clus1,self.clus2]

		'''
		Convert pair to 
		new format.
		'''

		for i in range(len(self.pair)):
			self.pair[i] = self.convert(self.pair[i])

	def convert(self,clus):

		newClus=[]

		for line in clus:
			ele,x,y,z = line.split()
			atom = [ele,float(x),float(y),float(z)]	
			newClus.append(atom)

		return newClus

	def prepare(self):

		'''
		Using the pair list rotate
		and the sort the cluster by
		the z coordinate.
		'''

		for i in range(len(self.pair)):
 			self.pair[i] = self.rotate(self.pair[i])
			self.pair[i] = self.sortZ(self.pair[i])

	def rotate(self,clus):

		'''
		Rotate cluster 
		about random axis.
		'''

		rotClus=[]

		theta = ran.uniform(0,np.pi*2)
		phi = ran.uniform(0,np.pi)

		rot11 = np.cos(phi)
		rot12 = 0.0
		rot13 = -np.sin(phi)
		rot21 = np.sin(theta)*np.sin(phi)
		rot22 = np.cos(theta)
		rot23 = np.sin(theta)*np.cos(phi)
		rot31 = np.cos(theta)*np.sin(phi)
		rot32 = -np.sin(theta)
		rot33 = np.cos(theta)*np.cos(phi)

		for i in range(len(clus)):
			ele, x, y, z = clus[i]
			rotX = rot11*x + rot12*y + rot13*z
			rotY = rot21*x + rot22*y + rot23*z
			rotZ = rot31*x + rot32*y + rot33*z
			rotAtom = [ele,rotX,rotY,rotZ]
			clus[i] = rotAtom

		return clus

	def sortZ(self,clus):

		'''
		Bubble sort by z.
		'''

		swapped = True

		while swapped:
			swapped=False
			for i in range(len(clus)-1):
				if clus[i][3] > clus[i+1][3]:
					temp = clus[i]
					clus[i] = clus[i+1]
					clus[i+1] = temp
					swapped = True

		return clus

	def getFitnessPair(self):
		
		self.fitPair=[]

		fitness = select(self.nPool).fitness

		self.fitPair.append(fitness[self.pairPos[0]])
		self.fitPair.append(fitness[self.pairPos[1]])

	def mate(self):

		'''
		Return offspring based 
		on crosstype.
		'''

		if len(self.eleNames) == 1:

			if self.crossType == "random":
				return self.monoRandom()
			elif self.crossType == "weighted":
				return self.monoWeighted()

		elif len(self.eleNames) == 2:

			if self.crossType == "random":
				return self.biRandom()
			elif self.crossType == "weighted":
				return self.biWeighted()
			# Old method.
			elif self.crossType == "Bimetallic":
				return self.CutSpliceBimetallic()

	def monoRandom(self):	

		'''
		Monometallic random 
		crossover.
		'''

		offspring=[]

		clus1 = self.pair[0]
		clus2 = self.pair[1]

		start = ran.randrange(self.natoms)

		for i in range(start):
			offspring.append(clus1[i])

		for j in range(start,self.natoms):
			offspring.append(clus2[j])

		return offspring

	def monoWeighted(self):

		'''
		Monometallic weighted crossover.
		'''

		self.getFitnessPair()

		offspring=[]

		fit1 = self.fitPair[0]
		fit2 = self.fitPair[1]

		clus1 = self.pair[0]
		clus2 = self.pair[1]

		start = int(self.natoms*(fit1/(fit1+fit2)))

		for i in range(start):
			offspring.append(clus1[i])

		for j in range(start,self.natoms):
			offspring.append(clus2[j])

		return offspring

	def biRandom(self):

		compositionWrong = True

		while compositionWrong:

			offspring = []

			self.getFitnessPair()

			fit1 = self.fitPair[0]
			fit2 = self.fitPair[1]

			clus1 = self.pair[0]
			clus2 = self.pair[1]

			# start = int(self.natoms*(fit1/(fit1+fit2)))
			start = ran.randrange(1,self.natoms)

			for i in range(start):
				offspring.append(clus1[i])

			for j in range(start,self.natoms):
				offspring.append(clus2[j]) 

			CheckEle = []

			for ele in self.eleNames:
				eleCount = 0
				for atom in offspring:
					if atom[0] == ele:
						eleCount += 1
				CheckEle.append(eleCount)

			if CheckEle == self.eleNums:

				compositionWrong = False

	def biWeighted(self):

		offspring = []

		self.getFitnessPair()

		fit1 = self.fitPair[0]
		fit2 = self.fitPair[1]

		plane = int(self.natoms*(fit1/(fit1+fit2)))

		'''
		Take initial cut from 
		the first cluster. 
		'''

		for i in range(plane):

			offspring.append(self.pair[0][i])

		'''
		Count the number of Elements 
		A and B needed from second cut. 
		'''

		checkEleNums = []

		for element in self.eleNames:
			eleCount = 0
			for atom in offspring:
				if atom[0] == element:
					eleCount += 1 
			checkEleNums.append(eleCount)

		'''
		Take second cut based on the 
		number of elements already in 
		offspring. 
		'''

		diffA = self.eleNums[0] - checkEleNums[0]
		diffB = self.eleNums[1] - checkEleNums[1]

		eleDiff = [diffA, diffB]

		'''
		If there are too many of one 
		element in offspring remove 
		the difference.
		'''

		for i in range(len(eleDiff)):
			if eleDiff[i] < 0:
				for j in range(abs(eleDiff[i])):
					for atom in offspring:
						if atom[0] == self.eleNames[i]:
							offspring.remove(atom)
							break


		for i in range(len(self.eleNames)):
			for j in range(eleDiff[i]):

				for atom in self.pair[1]:
					if atom[0] == self.eleNames[i] and atom not in offspring:

						offspring.append(atom)

						break

		return offspring

	def CutSpliceBimetallic(self):	

		''' Bimetallic Crossover. '''

		offspring = []

		clus1 = self.pair[0]
		clus2 = self.pair[1]

		if self.eleNums[0] % 2 == 0 and self.eleNums[1] % 2 == 0:
			c1_na = int(self.eleNums[0]) / 2
			c1_nb = int(self.eleNums[1]) / 2
			c2_na = int(self.eleNums[0]) / 2
			c2_nb = int(self.eleNums[1]) / 2
		elif self.eleNums[0] % 2 == 0 and self.eleNums[1] % 2 == 1:
			c1_na = int(self.eleNums[0]) / 2
			c1_nb = int(self.eleNums[1]) / 2
			c2_na = int(self.eleNums[0]) / 2
			c2_nb = int(self.eleNums[1]) / 2 + 1
		elif self.eleNums[0] % 2 == 1 and self.eleNums[1] % 2 == 0:
			c1_na = int(self.eleNums[0]) / 2
			c1_nb = int(self.eleNums[1]) / 2
			c2_na = int(self.eleNums[0]) / 2 + 1
			c2_nb = int(self.eleNums[1]) / 2
		elif self.eleNums[0] % 2 == 1 and self.eleNums[1] % 2 == 1:
			c1_na = int(self.eleNums[0]) / 2
			c1_nb = int(self.eleNums[1]) / 2
			c2_na = int(self.eleNums[0]) / 2 + 1
			c2_nb = int(self.eleNums[1]) / 2 + 1

		c1_nab = [c1_na,c1_nb]
		c2_nab = [c2_na,c2_nb]
	
		for i in range(2):
			start = 0 
			counter = 0
			for j in range(c1_nab[i]):
				for atom in clus1[start:]:
					counter += 1
					ele,x,y,z = atom
					if ele == self.eleNames[i]:
						offspring.append(atom)
						start = counter
						break

		for i in range(2):
			start = 0 
			counter = 0
			for j in range(c2_nab[i]):
				for atom in clus2[start:]:
					counter += 1
					ele,x,y,z = atom
					if ele == self.eleNames[i]:
						offspring.append(atom)
						start = counter
						break

		'''
		Sort offspring
		by element.
		'''

		sortOffspring = []

		for element in self.eleNames:
			for atom in offspring:
				ele,x,y,z = atom
				if ele == element:
					sortOffspring.append(atom)

		offspring = sortOffspring

		return offspring


