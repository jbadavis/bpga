'''
DFT input class.

Jack Davis

17/9/2014
'''

import sys 
import subprocess as sp

from CoM import CoM 

class vasp_input:

	'''
	Creates POSCAR input files 
	in directories from .xyz's
	'''

	def __init__(self,i,eleNames
		,eleMasses,eleNums):

		self.i = i
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.eleNums = eleNums

		self.read_xyz() 
		self.cell_size()
		self.write_poscar()

	def read_xyz(self):

		'''
		Reads previously created .xyz
		into class coord list.
		'''

		with open(str(self.i) + ".xyz") as xyz:
			self.natoms = xyz.readline()
			comment = xyz.readline()
			self.coords = xyz.readlines()

		self.coords = CoM(self.coords,self.eleNames,self.eleMasses)

	def cell_size(self):

		'''
		Box size required found by
		adding 10 to the largest 
		value in the coord list
		'''

		size = []

		for line in self.coords:
			ele, x, y, z = line.split()
			size.append(x)
			size.append(y)
			size.append(z)
		self.box = abs(float(max(size))) + 10.0

	def write_poscar(self):

		'''
		POSCAR is written, making 
		sure elements are printed
		in order of elements list
		'''

		self.eleNums = [str(i) for i in self.eleNums]

		#sp.call(["mkdir", str(self.i)])

		with open(str(self.i)+"/POSCAR","w") as poscar:
			poscar.write(str(self.i) + '\n')
			poscar.write(str(self.box) + '\n')
			poscar.write("1.0 0.0 0.0\n")
			poscar.write("0.0 1.0 0.0\n")
			poscar.write("0.0 0.0 1.0\n")
			poscar.write(" ".join(self.eleNames) + '\n')
			poscar.write(" ".join(self.eleNums) + '\n')
			poscar.write("Direct\n")
			for element in self.eleNames:
				for line in self.coords:
					ele, x, y, z = line.split()
					if ele == element:
						x = str( (float(x) + (self.box/2) ) / self.box )
						y = str( (float(y) + (self.box/2) ) / self.box )
						z = str( (float(z) + (self.box/2) ) / self.box )
						out_string = x + "  " + y + "  " + z + '\n'
						poscar.write(out_string) 
			sp.call(["cp", "INCAR" ,str(self.i)])
			sp.call(["cp", "KPOINTS" ,str(self.i)])
			sp.call(["cp", "POTCAR" ,str(self.i)])
