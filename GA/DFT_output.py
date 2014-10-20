#!/usr/bin/env python

'''
DFT output class for Ligand Mover.

Jack Davis

17/9/2014
'''

class vasp_output:

	'''
	Class to extract final
	energy and coordinated from 
	VASP OUTCAR file
	'''
	
	def __init__(self,i,natoms):
		
		self.final_coords = []	
		self.final_energy = 0.0
		self.natoms = int(natoms)
		self.check_calc(i)
		# self.read_energy(i)
		# self.read_coords(i)

	def check_calc(self,i):

		'''
		Check to see if VASP calculation
		has converged by searching OUTCAR
		for a string continuously
		'''

		finish_str = "reached required accuracy"
		errorStr = "Error EDDDAV:"
		end = False
		self.error = False

		with open(str(i) + "/OUTCAR","r") as outcar:
			while end == False:
				for line in outcar:
					if finish_str in line:
						end = True
						print "finished!"
					elif errorStr in line:
						self.error = True
						end = True  
				outcar.seek(0)

		if end and self.error == False:
			self.read_energy(i)
			self.read_coords(i)

	def read_energy(self,i):

		'''
		Returns final energy from
		convereged OUTCAR file
		'''

		energy_str = "energy  without entropy="

		with open(str(i) + "/OUTCAR","r") as outcar:
			for line in outcar:
				if energy_str in line:
					energy = line.split()
   		print "Found the final energy"
   		self.final_energy = energy[6]

	def read_coords(self,i):

		'''
		Finds final coordinates 
		and passes them back to the
		main program
		'''

		counter = 0
		found = False
		strucNums = []
		coord_str = " POSITION"

		with open(str(i) + "/OUTCAR","r") as outcar:
			outcarList = outcar.readlines()
		for line in outcarList:
			counter += 1
			if coord_str in line:
				strucNums.append(counter)

		# Find last element in list 
		final = len(strucNums) - 1

		top = strucNums[final] + 1
		bottom = top + (self.natoms)  

		for line in outcarList[top:bottom]:
			xyz = line.split()
			self.final_coords.append(xyz[0])
			self.final_coords.append(xyz[1])
			self.final_coords.append(xyz[2])
		print "Found final coordinates"
