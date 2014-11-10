'''
Explode

Jack Davis

21/8/14
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
		Check if atoms 
		overlapping.
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

	def overlap(self):

		'''
		Check if cluster 
		is exploded.
		'''

		start = 0

		for i in range(self.natoms):
			finish = start + self.natoms 
			bonds = self.r[start:finish]
			start += self.natoms
			tooLong = 0
			for bond in bonds:
				if float(bond) < 1.5 and float(bond) != 0.:
					return True

		return False

# def exploded(natoms,coords):

# 	bonds=[]
# 	r=[]

# 	if len(coords) == natoms:
# 		newCoords = []
# 		for line in coords:
# 			ele,x,y,z = line.split()
# 			newCoords.append(x)
# 			newCoords.append(y)
# 			newCoords.append(z)
# 		coords = newCoords

# 	coords = [float(i) for i in coords]

# 	for i in range(0,len(coords),3):
# 		x1 = float(coords[i])
# 		y1 = float(coords[i+1])
# 		z1 = float(coords[i+2])
# 		for j in range(0,len(coords),3):
# 			x2 = float(coords[j])
# 			y2 = float(coords[j+1])
# 			z2 = float(coords[j+2])

# 			x2 -= x1
# 			y2 -= y1
# 			z2 -= z1

# 			r.append(np.sqrt( x2**2 + y2**2 + z2**2 ))

# 	start = 0

# 	for i in range(natoms):
# 		finish = start + natoms 
# 		bonds = r[start:finish]
# 		start += natoms
# 		tooLong = 0
# 		for bond in bonds:
# 			if float(bond) > 3.0:
# 				tooLong += 1
# 		if tooLong == natoms-1:
# 			return True

# 	return False

# def overlap(natoms,coords):

# 	bonds=[]
# 	r=[]

# 	if len(coords) == natoms:
# 		newCoords = []
# 		for line in coords:
# 			ele,x,y,z = line.split()
# 			newCoords.append(x)
# 			newCoords.append(y)
# 			newCoords.append(z)
# 		coords = newCoords

# 	coords = [float(i) for i in coords]

# 	for i in range(0,len(coords),3):
# 		x1 = float(coords[i])
# 		y1 = float(coords[i+1])
# 		z1 = float(coords[i+2])
# 		for j in range(0,len(coords),3):
# 			x2 = float(coords[j])
# 			y2 = float(coords[j+1])
# 			z2 = float(coords[j+2])

# 			x2 -= x1
# 			y2 -= y1
# 			z2 -= z1

# 			r.append(np.sqrt( x2**2 + y2**2 + z2**2 ))

# 	start = 0

# 	print r

# 	for i in range(natoms):
# 		finish = start + natoms 
# 		bonds = r[start:finish]
# 		start += natoms
# 		tooLong = 0
# 		for bond in bonds:
# 			if float(bond) < 1. and float(bond) != 0.:
# 				return True

# 	return False
