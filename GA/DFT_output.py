#!/usr/bin/env python

'''
DFT output class.

Jack Davis

17/9/2014
'''

class vasp_output:

	'''
	Class to extract final
	energy and coordinated from 
	VASP OUTCAR file
	'''
	
	def __init__(self,calcNum,natoms):

		self.calcNum = calcNum
		self.natoms = int(natoms)

	def checkError(self):

		errorStr = "Error EDDDAV:"

		with open(str(self.calcNum) + "/OUTCAR","r") as outcar:
			for line in outcar:
				if errorStr in line:
					error = True
				else:
					error = False

		return error

	def getEnergy(self):

		'''
		Returns final energy from
		convereged OUTCAR file
		'''

		energy_str = "energy  without entropy="

		with open(str(self.calcNum) + "/OUTCAR","r") as outcar:
			for line in outcar:
				if energy_str in line:
					energy = line.split()
   		print "Found the final energy"

   		return energy[6]

	def getCoords(self):

		'''
		Finds final coordinates 
		and passes them back to the
		main program
		'''

		return self.gasCoords()

	def surfCoords(self):

		'''
		For surface. 
		'''

		pass

	def gasCoords(self):

		'''
		For gas phase.
		'''

		counter = 0
		strucNums = []
		finalCoords = []
		coord_str = " POSITION"

		with open(str(self.calcNum) + "/OUTCAR","r") as outcar:
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
			finalCoords.append(xyz[0])
			finalCoords.append(xyz[1])
			finalCoords.append(xyz[2])
		
		return finalCoords
