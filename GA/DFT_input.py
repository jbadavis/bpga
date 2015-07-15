'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

17/9/2014

--- VASP Input Class ---

'''

import sys 
import subprocess as sp

from CoM import CoM 

class vasp_input:

	'''
	Creates POSCAR input files 
	in directories from .xyz's
	'''

	def __init__(self,calcNum
				,clus,eleNames
				,eleMasses,eleNums
				,boxAdd):

		self.calcNum = str(calcNum)
		self.clus = clus
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.eleNums = eleNums
		self.boxAdd = boxAdd

		self.cell_size()
		self.write_poscar()

	def cell_size(self):

		'''
		Box size required found by
		adding 10 to the largest 
		value in the coord list
		'''

		self.clus = CoM(self.clus,self.eleNames,self.eleMasses)

		size = []

		for atom in self.clus:
			ele,x,y,z = atom
			size.append(abs(float(x)))
			size.append(abs(float(y)))
			size.append(abs(float(z)))
		self.box = max(size) + self.boxAdd

	def write_poscar(self):

		'''
		POSCAR is written, making 
		sure elements are printed
		in order of elements list
		'''

		self.eleNums = [str(i) for i in self.eleNums]

		with open(self.calcNum+"/POSCAR","w") as poscar:

			poscar.write(self.calcNum + '\n')
			poscar.write(str(self.box) + '\n')

			poscar.write("1.0 0.0 0.0\n")
			poscar.write("0.0 1.0 0.0\n")
			poscar.write("0.0 0.0 1.0\n")

			poscar.write(" ".join(self.eleNames) + '\n')
			poscar.write(" ".join(self.eleNums) + '\n')

			'''
			Coordinates are written 
			in lattice coordinates.
			'''

			poscar.write("Direct\n")

			for element in self.eleNames:
				for atom in self.clus:
					ele,x,y,z = atom
					if ele == element:
						x = str( ( x + (self.box/2) ) / self.box )
						y = str( ( y + (self.box/2) ) / self.box )
						z = str( ( z + (self.box/2) ) / self.box )
						out_string = x + "  " + y + "  " + z + '\n'
						poscar.write(out_string) 

			os.system("cp {POTCAR,INCAR,KPOINTS} "+self.calcNum)

