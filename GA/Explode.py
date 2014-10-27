'''
Explode

Jack Davis

21/8/14
'''

import numpy as np

def exploded(natoms,vaspOUT):

	coords=[]
	bonds=[]
	r=[]

	for line in vaspOUT:
		x,y,z = line.split()
		x = float(x)
		y = float(y)
		z = float(z)
		coords.append(x)
		coords.append(y)
		coords.append(z)

	for i in range(0,len(coords),3):
		x1 = float(coords[i])
		y1 = float(coords[i+1])
		z1 = float(coords[i+2])
		for j in range(0,len(coords),3):
			x2 = float(coords[j])
			y2 = float(coords[j+1])
			z2 = float(coords[j+2])

			x2 -= x1
			y2 -= y1
			z2 -= z1

			r.append(np.sqrt( x2**2 + y2**2 + z2**2 ))

	start = 0

	for i in range(natoms):
		finish = start + natoms 
		bonds = r[start:finish]
		start += natoms
		tooLong = 0
		for bond in bonds:
			if float(bond) > 3.0:
				tooLong += 1
		if tooLong == natoms-1:
			return True

	return False
