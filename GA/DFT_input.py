#!/usr/bin/env python

'''
DFT input class.

Jack Davis

17/9/2014
'''

import sys 
import subprocess as sp

class vasp_input:

	'''
	Creates POSCAR input files in directories from .xyz's
	'''

	def __init__(self,i):

		self.i = i

		self.elements = []
		self.ele_num = []
		self.eleXYZ = []

		self.read_xyz() 
		self.count_elements()
		self.cell_size()
		self.write_poscar()


	def read_xyz(self):

		'''
		Reads previously created .xyz
		into class coord list
		'''

		with open(str(self.i) + ".xyz") as xyz:
			# Read number of atoms from line 1 of xyz.
			self.natoms = xyz.readline()
			# Read comment from line 2 of xyz.
			comment = xyz.readline()
			# Read coordinates into list.
			self.coords = xyz.readlines()

	def count_elements(self):

		'''
		Using the class coord list
		the number of different 
		elements is counted
		'''

		counter = 0

		# Adds all different ele names to list.
		for line in self.coords: 
			ele, x, y, z = line.split()
			if counter == 0:
				self.elements.append(ele)
			elif counter > 0:
				if ele not in self.elements:
					self.elements.append(ele)
			counter += 1

		# Counts number of instances of each ele. 
		for element in self.elements: 
			counter = 0
			for line in self.coords: 
				ele, x, y, z = line.split()
				if element == ele:
					counter += 1
			self.ele_num.append(str(counter))

		for i in range(len(self.elements)):
			for j in range(int(self.ele_num[i])):
				self.eleXYZ.append(self.elements[i])
	
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

		#sp.call(["mkdir", str(self.i)])

		with open(str(self.i)+"/POSCAR","w") as poscar:
			poscar.write(str(self.i) + '\n')
			poscar.write(str(self.box) + '\n')
			poscar.write("1.0 0.0 0.0\n")
			poscar.write("0.0 1.0 0.0\n")
			poscar.write("0.0 0.0 1.0\n")
			poscar.write(" ".join(self.elements) + '\n')
			poscar.write(" ".join(self.ele_num) + '\n')
			poscar.write("Direct\n")
			for element in self.elements:
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

class qe_input:

	"""
	Creates .in for Quantum Espresso 
	Calculations - requires DFT.in
	containing input parameters
	"""

	def __init__(self,i):
		self.i = i
		self.qe_input()

	def qe_input(self):
		with open("DFT.in",'r') as dft:
			xyz = open(str(self.i) + ".xyz",'r')
			qe_out = open(str(self.i) + ".in",'w')
			coords = xyz.readlines()
			for line in dft:
				if "coordinates" in line:
					for line in coords[2:]:
						qe_out.write(line)
				qe_out.write(str(line))
		
