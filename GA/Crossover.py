'''
Daven and Ho 
Crossover class

Jack Davis

14/10/14
'''

import numpy as np
import random as ran

from checkPool import checkPool
from CoM import CoM 

import sys

class crossover:

	def __init__(self
				,clus1
				,clus2
				,eleNums
				,eleNames
				,natoms
				,pair):

		ran.seed()

		'''Convert list format '''
		clus1 = self.convert(clus1)
		clus2 = self.convert(clus2)

		self.pair = [clus1,clus2]

		self.eleNames = eleNames
		self.eleNums = eleNums
		self.natoms = natoms 
		self.pairPos = pair

		''' Rotate and sort pair of clusters'''
		self.prepare()

	def convert(self,clus):

		newClus=[]

		for line in clus:
			ele,x,y,z = line.split()
			atom = [ele,float(x),float(y),float(z)]	
			newClus.append(atom)

		return newClus

	def fitness(self):
		
		energies=[]
		fitness=[]
		self.fitPair=[]

		getEn = checkPool()
		energies = getEn.energies

		energies = sorted(energies)
		minEn = energies[0]
		rangeEn = energies[len(energies)-1] - energies[0]

		for energy in energies:
			fit=0.5*(1-np.tanh(2.*((energy-minEn)/rangeEn)-1.))
			fitness.append(fit)

		self.fitPair.append(fitness[self.pairPos[0]])
		self.fitPair.append(fitness[self.pairPos[1]])

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

		for atom in clus:
			ele, x, y, z = atom
			rotX = rot11*x + rot12*y + rot13*z
			rotY = rot21*x + rot22*y + rot23*z
			rotZ = rot31*x + rot32*y + rot33*z
			rotAtom = [ele,rotX,rotY,rotZ]
			rotClus.append(rotAtom)

		return rotClus

	def sortZ(self,clus):

		'''
		Sort cluster by
		z-axis.
		'''

		zList = []
		sortedClus = []

		for atom in clus:
			ele,x,y,z = atom
			zList.append(z)

		zList.sort()

		for sortedZ in zList:
			for atom in clus: 
				ele,x,y,z = atom
				if z == sortedZ:
					sortedClus.append(atom)

		return sortedClus

	def CutSpliceRandom(self):	

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

	def CutSpliceWeighted(self):

		'''
		Monometallic weighted crossover.
		'''

		self.fitness()

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
