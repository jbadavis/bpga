'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

21/8/14

--- Check Cluster Class ---

'''

import numpy as np

class checkClus:
	
	'''
	Checks if cluster
	is overlaping 
	or exploded.

	checkType is 
	either overlap
	or exploded
	'''

	def __init__(self,natoms,coords):

		self.natoms = natoms
		self.coords = coords
		self.r = []

		self.getBonds()

	def getBonds(self):

		'''
		Get all bond 
		lengths for a 
		cluster.
		'''

		if len(self.coords) == self.natoms:
			newCoords = []
			for line in self.coords:
				ele,x,y,z = line.split()
				newCoords.append(x)
				newCoords.append(y)
				newCoords.append(z)
			self.coords = newCoords

		self.coords = [float(i) for i in self.coords]

		for i in range(0,len(self.coords),3):
			x1 = float(self.coords[i])
			y1 = float(self.coords[i+1])
			z1 = float(self.coords[i+2])
			for j in range(0,len(self.coords),3):
				x2 = float(self.coords[j])
				y2 = float(self.coords[j+1])
				z2 = float(self.coords[j+2])

				x2 -= x1
				y2 -= y1
				z2 -= z1

				self.r.append(np.sqrt( x2**2 + y2**2 + z2**2 ))

	def exploded(self):

		'''
		Return true if cluster has 
		exploded
		'''

		start = 0

		for i in range(self.natoms):
			finish = start + self.natoms 
			bonds = self.r[start:finish]
			start += self.natoms
			tooLong = 0
			for bond in bonds:
				if float(bond) > 3.0:
					tooLong += 1
			if tooLong == self.natoms-1:
				return True

		return False
