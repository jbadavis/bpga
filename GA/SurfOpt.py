'''
Surface GA Class

Jack Davis

18/3/15
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

		self.clus = self.reFormat(clus)

		self.surfaceXYZ = surface.getSurf() 
		self.lat = surface.lat

		''' Surface layers in x,y and z '''

		self.x = surface.x
		self.y = surface.y
		self.z = surface.z

		self.height = 1.

	def reFormat(self,clus):

		'''
		XYZ string format changed 
		to atom formant.
		'''

		for i in range(len(clus)):

			ele,x,y,z = clus[i].split()
			atom = [ele,float(x),float(y),float(z)]

			clus[i] = atom

		clus = CoM(clus,self.eleNames,self.eleMasses)

		return clus

	def placeClus(self):

		self.surfClus = self.clus + self.surfaceXYZ

		self.getBonds()

		'''
		Return cluster surface system 
		at fixed height.
		'''

		return self.fix()

	def getBonds(self):

		'''
		Gets all bond lengths for 
		the cluster-surface system.
		'''

		bonds=[]
		elePairs=[]

		self.metalSurfBonds=[]

		for i in self.surfClus:
			ele1,x1,y1,z1 = i
			for j in self.surfClus:
				if i == j:
					pass
				else:      
					ele2,x2,y2,z2 = j
					x2 -= x1
					y2 -= y1
					z2 -= z1
					r = np.sqrt(x2**2 + y2**2 + z2**2)
					if r not in bonds:
						elePair = [ele1,ele2]
						bonds.append(r)
						elePairs.append(elePair)

		for metal in self.eleNames:
			for i in range(len(elePairs)):
				if metal in elePairs[i] and "Mg" in elePairs[i]:
					self.metalSurfBonds.append(bonds[i])
				elif metal in elePairs[i] and "O" in elePairs[i]:
					self.metalSurfBonds.append(bonds[i])

	def fix(self):

		'''
		Raises or lowers the cluster
		above the surface.
		'''

		self.fixedSurfClus=[]

		# diff = self.height - min(self.metalSurfBonds)

		for atom in self.surfClus:
			ele,x,y,z, = atom
			if ele in self.eleNames:
				x = x + (self.x * self.lat/2) / 2
				y = y + (self.y * self.lat/2) / 2
				z += self.height + (self.z * self.lat/2)
				newAtom = [ele,x,y,z]
				self.fixedSurfClus.append(newAtom)
			else:
				self.fixedSurfClus.append(atom)

		return self.fixedSurfClus
