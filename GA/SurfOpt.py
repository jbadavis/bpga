'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

8/6/15

--- Surface Optimiser Class ---

'''

import sys
import numpy as np

from CoM import CoM

class SurfOpt:

	def __init__(self
				,clus
				,surface
				,eleNames
				,eleMasses):
		

		self.eleNames = eleNames
		self.eleMasses = eleMasses

		self.clus = CoM(clus,self.eleNames,self.eleMasses)

		self.surfaceXYZ = surface.getSurf() 

		self.lat = surface.lat

		''' Surface layers in x,y and z '''

		self.x = surface.x
		self.y = surface.y
		self.z = surface.z

		self.height = surface.clusHeight
		

	def placeClus(self):

		self.fix()

		'''
		Return cluster surface system 
		'''

		return self.clus + self.surfaceXYZ

	def fix(self):

		'''
		Raises or lowers the cluster
		above the surface.
		'''

		'''
		Get minimum Z coordinate.
		'''

		clusZ = []

		for atom in self.clus:
			clusZ.append(atom[3])

		minClusZ = min(clusZ)

		'''
		Get max surface height.
		'''

		maxSurfZ = self.lat/2 * (self.z-1)

		'''
		Calculate difference and adjust 
		cluster Z.
		'''

		diff =  (maxSurfZ - minClusZ) + self.height

		for i in range(len(self.clus)):
			ele,x,y,z, = self.clus[i]
			x = x + (self.x * self.lat/2) / 2
			y = y + (self.y * self.lat/2) / 2		
			z += diff 
			atom = [ele,x,y,z]
			self.clus[i] = atom

		# for atom in self.surfClus:
		# 	ele,x,y,z, = atom
		# 	if ele in self.eleNames:
		# 		x = x + (self.x * self.lat/2) / 2
		# 		y = y + (self.y * self.lat/2) / 2
		# 		z += self.height + (self.z * self.lat/2)
		# 		newAtom = [ele,x,y,z]
		# 		self.fixedSurfClus.append(newAtom)
		# 	else:
		# 		self.fixedSurfClus.append(atom)

		# return self.fixedSurfClus

	# def getBonds(self):

	# 	'''
	# 	Gets all bond lengths for 
	# 	the cluster-surface system.
	# 	'''

	# 	bonds=[]
	# 	elePairs=[]

	# 	self.metalSurfBonds=[]

	# 	for i in self.surfClus:
	# 		ele1,x1,y1,z1 = i
	# 		for j in self.surfClus:
	# 			if i == j:
	# 				pass
	# 			else:      
	# 				ele2,x2,y2,z2 = j
	# 				x2 -= x1
	# 				y2 -= y1
	# 				z2 -= z1
	# 				r = np.sqrt(x2**2 + y2**2 + z2**2)
	# 				if r not in bonds:
	# 					elePair = [ele1,ele2]
	# 					bonds.append(r)
	# 					elePairs.append(elePair)

	# 	for metal in self.eleNames:
	# 		for i in range(len(elePairs)):
	# 			if metal in elePairs[i] and "Mg" in elePairs[i]:
	# 				self.metalSurfBonds.append(bonds[i])
	# 			elif metal in elePairs[i] and "O" in elePairs[i]:
	# 				self.metalSurfBonds.append(bonds[i])
