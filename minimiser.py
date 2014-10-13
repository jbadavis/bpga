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

		self.stride = self.natoms + 2

		for i in range(10):

			strucNum = 0
			
			self.checkDB
			self.lockDB

			self.readPool()

			self.unlockDB

			for line in self.poolList:		
				strucNum += 1
				if "NotMinimised" in line:

					# print "found line"
					# status, strucNum = line.split()
					self.minimiseXYZ(strucNum)

					break

	def minimiseXYZ(self,strucNum):

		stride = self.stride
		xyzNum = ((strucNum-1)/stride) + 1

		'''
		Grab structure 
		from pool.dat
		and write .xyz.
		'''

		self.checkDB
		self.lockDB
		
		initialXYZ = self.poolList[strucNum-2:strucNum+stride-2]
		
		self.unlockDB

		with open(str(xyzNum)+".xyz","w") as xyzFile:
			for line in initialXYZ:
				xyzFile.write(line)

		'''
		Write Running flag 
		to pool and start 
		DFT calculation.
		'''

		self.checkDB
		self.lockDB

		# Write Running flag to pool.dat
		self.readPool()
		self.poolList[strucNum-1] = "Running\n"
		self.writePool()

		self.unlockDB

		# Run DFT calc
		vaspIN = DFTin.vasp_input(xyzNum)
		run = DFTsub.submit()
		run.archer(xyzNum,self.mpitasks)
		vaspOUT = DFTout.vasp_output(xyzNum,self.natoms)

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		self.checkDB
		self.lockDB

		self.readPool()

		# Write final energy to pool.dat
		energy = vaspOUT.final_energy
		# Write final structure(minus element types)
		finalXYZ = vaspOUT.final_coords
		# Get element types and debox
		finalXYZele = self.finalCoords(initialXYZ[2:],finalXYZ,vaspIN.box)
		# Update pool 
		self.poolList[strucNum:strucNum+stride-2] = finalXYZele
		self.poolList[strucNum-1] = "Finished Energy = " + str(energy) + "\n"
		self.writePool()

		self.unlockDB

	def finalCoords(self,initialXYZ,finalXYZ,box):

		'''
		Adds element types 
		to final coordinates
		from OUTCAR. Removes 
		from centre of box
		'''

		eleList = []
		finalXYZele =[]

		for line in initialXYZ:
			ele, x,y,z = line.split()
			eleList.append(ele)

		# Take coords out of centre of box.
		finalXYZ = [float(i) - box/2 for i in finalXYZ]
		# Convert list to str for writing to pool.
		finalXYZ = [str(i) for i in finalXYZ]

		for i in range(0,len(finalXYZ),3):
			xyz = str(finalXYZ[i]) + " " \
			+ str(finalXYZ[i+1]) + " " \
			+ str(finalXYZ[i+2]) + "\n"
			xyzLine = eleList[i/3] + " " + xyz
			finalXYZele.append(xyzLine)

		return finalXYZele

	def readPool(self):

		'''
		Reads pool at beginning/
		throughout calculation.
		'''


		with open("pool.dat","r") as pool:
			self.poolList = pool.readlines()

	def writePool(self):

		'''
		Writes pool to
		file after any
		changes.
		'''

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
