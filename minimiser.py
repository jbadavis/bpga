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

	def checkDatabase(self):

		strucNum = 0
		self.stride = self.natoms + 2

		for i in range(10):

			self.readPool()

			for line in self.poolList:
				strucNum += 1
				if "NotMinimised" in line:
					status, strucNum = line.split
					print self.poolList
					print strucNum
					self.minimiseXYZ(strucNum)

				break

	def minimiseXYZ(self,strucNum):

		stride = self.stride

		xyzNum = ((strucNum-1)/stride) + 1

		self.checkDB
		self.lockDB
		
		xyz = self.poolList[strucNum-2:strucNum+stride-2]
		
		self.unlockDB

		with open(str(xyzNum)+".xyz","w") as xyzFile:
			for line in xyz:
				xyzFile.write(line)

		self.checkDB
		self.lockDB

		# Write Running to pool.dat
		self.readPool()
		self.poolList[strucNum-1] = "Running\n"
		self.writePool()

		self.unlockDB

		# Run DFT calc
		vaspIN = DFTin.vasp_input(xyzNum)
		run = DFTsub.submit()
		run.archer(xyzNum,self.mpitasks)
		vaspOUT = DFTout.vasp_output(xyzNum,self.natoms)

		self.checkDB
		self.lockDB

		# Write final energy to pool.dat
		energy = vaspOUT.final_energy

		self.readPool()
		self.poolList[strucNum-1] = "Finished Energy = " + str(energy) + "\n"
		self.writePool()

		self.unlockDB

	def readPool(self):

		with open("pool.dat","r") as pool:
			self.poolList = pool.readlines()

	def writePool(self):

		with open("pool.dat","w") as pool:
			for line in self.poolList:
				pool.write(line)

	def lockDB(self):

		with open("lock.db","w") as lock:
			lock.write("locked")

	def unlockDB(self):

		os.system("rm lock.db")

	def checkDB(self):

		while os.path.exists("Lock.dat"):
			pass 
		else:
			print "closed"
