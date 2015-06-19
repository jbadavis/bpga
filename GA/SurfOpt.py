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

