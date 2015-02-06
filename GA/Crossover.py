'''
Daven and Ho 
Crossover class

Jack Davis

14/10/14
'''

import numpy as np
import random as ran

from checkPool import checkPool

class crossover:

	def __init__(self,clus1
				,clus2,eleNums
				,eleNames,natoms
				,pair):

		ran.seed()
		
		self.clus1 = clus1
		self.clus2 = clus2
		self.pair = [clus1,clus2]
		self.eleNames = eleNames
		self.eleNums = eleNums
		self.natoms = natoms 
		self.pairPos = pair
		self.offspring = []

		self.CheckComp()
		# self.fitness()
		self.prepare()

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
			ele, x, y, z = clus[i].split()
			x, y, z = float(x), float(y), float(z)
			rotX = rot11*x + rot12*y + rot13*z
			rotY = rot21*x + rot22*y + rot23*z
			rotZ = rot31*x + rot32*y + rot33*z
			newLine = ele + " " + str(rotX) + " " \
			+ str(rotY) + " " + str(rotZ) + "\n"
			clus[i] = newLine

		return clus

	def sortZ(self,clus):

		'''
		Sort cluster by
		z-axis.
		'''

		zList = []
		sortedClus = []

		for line in clus:
			ele,x,y,z = line.split()
			zList.append(float(z))
			sortedZlist = sorted(zList)

		sortedZlist = [str(i) for i in sortedZlist]

		for sortZ in sortedZlist:
			for line in clus: 
				ele,x,y,z = line.split()
				if sortZ == z:
					sortedClus.append(line)

		return sortedClus

	def CutSpliceRandom(self):	

		# Monometallic
		start = ran.randrange(self.natoms)

		for i in range(start):
			self.offspring.append(self.clus1[i])

		for j in range(start,self.natoms):
			self.offspring.append(self.clus2[j])

		return self.offspring

	def CutSpliceWeighted(self):

		self.fitness()

		# Monometallic
		fit1 = self.fitPair[0]
		fit2 = self.fitPair[1]

		start = self.natoms*(fit1/(fit1+fit2))
		start = int(start)

		for i in range(start):
			self.offspring.append(self.clus1[i])

		for j in range(start,self.natoms):
			self.offspring.append(self.clus2[j])

		return self.offspring

	# def BiCutSpliceWeighted(self):

	# 	self.fitness()

	# 	fit1 = self.fitPair[0]
	# 	fit2 = self.fitPair[1]

	# 	cut = self.natoms*(fit1/(fit1+fit2))
	# 	cut = int(cut)

	# 	for i in range(cut):
	# 		self.offspring.append(self.clus1[i])

	# 	for j in range(cut,self.natoms):
	# 		self.offspring.append(self.clus2[j])

	# 	print self.offspring

	def CutSplice(self):	

		# Monometallic
		if len(self.eleNum) == 1:
			if self.eleNum[0] % 2 == 0:
				c1_na = int(self.eleNum[0]) / 2
				c2_na = int(self.eleNum[0]) / 2
			elif self.eleNum[0] % 2 == 1:
				c1_na = int(self.eleNum[0]) / 2
				c2_na = int(self.eleNum[0]) / 2 + 1

			start = 0 
			counter = 0
			for j in range(c1_na):
				for line in self.clus1[start:]:
					counter += 1
					ele,x,y,z = line.split()
					if ele == self.eleName[0]:
						self.offspring.append(line)
						start = counter
						break

			start = 0 
			counter = 0
			for j in range(c2_na):
				for line in self.clus2[start:]:
					counter += 1
					ele,x,y,z = line.split()
					if ele == self.eleName[0]:
						self.offspring.append(line)
						start = counter
						break

		# Bimetallic
		elif len(self.eleNum) == 2: 
			if self.eleNum[0] % 2 == 0 and self.eleNum[1] % 2 == 0:
				c1_na = int(self.eleNum[0]) / 2
				c1_nb = int(self.eleNum[1]) / 2
				c2_na = int(self.eleNum[0]) / 2
				c2_nb = int(self.eleNum[1]) / 2
			elif self.eleNum[0] % 2 == 0 and self.eleNum[1] % 2 == 1:
				c1_na = int(self.eleNum[0]) / 2
				c1_nb = int(self.eleNum[1]) / 2
				c2_na = int(self.eleNum[0]) / 2
				c2_nb = int(self.eleNum[1]) / 2 + 1
			elif self.eleNum[0] % 2 == 1 and self.eleNum[1] % 2 == 0:
				c1_na = int(self.eleNum[0]) / 2
				c1_nb = int(self.eleNum[1]) / 2
				c2_na = int(self.eleNum[0]) / 2 + 1
				c2_nb = int(self.eleNum[1]) / 2
			elif self.eleNum[0] % 2 == 1 and self.eleNum[1] % 2 == 1:
				c1_na = int(self.eleNum[0]) / 2
				c1_nb = int(self.eleNum[1]) / 2
				c2_na = int(self.eleNum[0]) / 2 + 1
				c2_nb = int(self.eleNum[1]) / 2 + 1

			c1_nab = [c1_na,c1_nb]
			c2_nab = [c2_na,c2_nb]
		
			for i in range(2):
				start = 0 
				counter = 0
				for j in range(c1_nab[i]):
					for line in self.clus1[start:]:
						counter += 1
						ele,x,y,z = line.split()
						if ele == self.eleName[i]:
							self.offspring.append(line)
							start = counter
							break

			for i in range(2):
				start = 0 
				counter = 0
				for j in range(c2_nab[i]):
					for line in self.clus2[start:]:
						counter += 1
						ele,x,y,z = line.split()
						if ele == self.eleName[i]:
							self.offspring.append(line)
							start = counter
							break

		'''
		Sort offspring
		by element.
		'''

		sortOffspring = []

		for element in self.eleName:
			for line in self.offspring:
				ele,x,y,z = line.split()
				if ele == element:
					sortOffspring.append(line)

		self.offspring = sortOffspring

		return self.offspring
						
	def CheckComp(self):

		self.eleName = []
		self.eleNum = []

		# Element types
		for i in range(len(self.clus1)):
			ele,x,y,z = self.clus1[i].split()
			if ele not in self.eleName:
				self.eleName.append(ele)

		# Element numbers
		for element in self.eleName: 
			counter = 0
			for line in self.clus1: 
				ele,x,y,z = line.split()
				if element == ele:
					counter += 1
			self.eleNum.append(int(counter))
