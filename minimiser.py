'''
Minimiser

Jack Davis

10/10/14
'''

import os
import DFT_input as DFTin
import DFT_output as DFTout
import DFT_submit as DFTsub

class minimiser:

	def __init__(self,natoms):
		
		self.natoms = natoms
		self.mpitasks = 24

		self.checkDatabase()

		self.initialXYZ()

	# def checkDatabase(self):

	# 	lock = os.path.exists("Lock.dat")

	# 	if lock == False:
	# 		f = open("Lock.dat","w")

	# 	while os.path.exists("Lock.dat"):
	# 		pass 
	# 	else:
			# print "closed"

	def checkDatabase(self):

		self.strucNum = 0
		self.stride = self.natoms + 2

		with open("pool.dat","r") as pool:
			self.poolList = pool.readlines()
			for line in self.poolList:
				self.strucNum += 1
				if "Not Minimised" in line:
					self.minimiseXYZ()
				else:
					print "****FINISHED!!!*****"

	def minimiseXYZ(self):

		strucNum = self.strucNum
		stride = self.stride

		xyzNum = ((strucNum-1)/stride) + 1
		
		xyz = self.poolList[strucNum-2:strucNum+stride-2]
		
		with open(str(xyzNum)+".xyz","w") as xyzFile:
			for line in xyz:
				xyzFile.write(line)

		self.poolList[strucNum-1] = "Running\n"

		with open("pool.dat","w") as pool:
			for line in self.poolList:
				pool.write(line)

		vaspIN = DFTin.vasp_input(xyzNum)
		run = DFTsub.submit()
		run.archer(xyzNum,self.mpitasks)
		vaspOUT = DFTout.vasp_output(xyzNum,self.natoms)

		energy = vaspOUT.final_energy

		self.poolList[strucNum-1] = "Finished Energy = " + str(energy) + "\n"

		with open("pool.dat","w") as pool:
			for line in self.poolList:
				pool.write(line)

