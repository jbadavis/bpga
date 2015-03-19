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
				,eleNames):
		
		self.clus = clus
		self.eleNames = eleNames

		self.surfaceXYZ = surface.getSurf() 
		self.lat = surface.lat

		''' Surface layers in x,y and z '''

		self.x = surface.x
		self.y = surface.y
		self.z = surface.z

		self.height = 1.

		self.plainClus = []

		self.RemoveXYZstuff()

	def RemoveXYZstuff(self):

		'''
		This needs to standardised 
		across the program.
		'''

		for line in self.clus:

			ele,x,y,z = line.split()
			newLine = [ele,float(x),float(y),float(z)]

			self.plainClus.append(newLine)

	def placeClus(self):

		self.surfClus = self.plainClus + self.surfaceXYZ

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

	# def makeXYZfile(self):

	# 	''' 
	# 	Convert list into XYZ file
	# 	'''

	# 	xyzFile = []

	# 	natoms = str(len(self.fixedSurfClus))

	# 	xyzFile.append(natoms+"\n\n")

	# 	for line in self.fixedSurfClus:

	# 		ele, x, y, z = line 

	# 		x = str(x)
	# 		y = str(y)
	# 		z = str(z)

	# 		newLine = ele+" "+x+" "+y+" "+z+"\n"

	# 		xyzFile.append(newLine)

	# 	return xyzFile
