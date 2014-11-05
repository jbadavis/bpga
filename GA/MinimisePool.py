'''
Minimise Pool

Jack Davis

20/10/14
'''

import os
import random as ran

import Database as db

import DFT_output as DFTout
import DFT_submit as DFTsub

from DFT_input import vasp_input as DFTin

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 
from Explode import exploded

class minPool:

	def __init__(self,natoms,r_ij,eleNums,eleNames
		,eleMasses,n,stride,hpc,mpitasks):
		
		self.natoms = natoms
		self.r_ij = r_ij
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.hpc = hpc
		self.mpitasks = mpitasks

		self.runCalc()

	def runCalc(self):

		self.findStruc()

	def findStruc(self):

		self.strucNum = 0
			
		db.check()
		db.lock()

		self.readPool()

		for line in self.poolList:		
			self.strucNum += 1
			if "NotMinimised" in line:

				self.xyzNum = ((self.strucNum-1)/self.stride) + 1

				if os.path.exists(str(self.xyzNum)) and "Restart" not in line:
						db.unlock()
						break
				else:
					self.poolList[self.strucNum-1] = "Running\n"
					self.writePool()
					# This causes excess cannot mkdir errors. 
					os.system("mkdir " + str(self.xyzNum))
					db.unlock()

				self.getXYZ()
				self.minimise()
				break

		if os.path.exists("lock.db"): 
			db.unlock()

	def getXYZ(self):

		'''
		Grab structure 
		from pool.dat
		and write .xyz.
		'''
		
		self.initialXYZ = self.poolList[self.strucNum-2:self.strucNum+self.stride-2]
		
		with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			for line in self.initialXYZ:
				xyzFile.write(line)

	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		self.vaspIN = DFTin(self.xyzNum,self.eleNames
					,self.eleMasses,self.eleNums)

		run = DFTsub.submit(self.hpc,self.xyzNum,self.mpitasks)
		self.vaspOUT = DFTout.vasp_output(self.xyzNum,self.natoms)


		'''
		Check for errors in DFT.
		Check if cluster has exploded.
		Update pool!
		'''

		if self.vaspOUT.error:
			print "*- Error in VASP Calculation -*"
			self.genRandom()
		elif exploded(self.natoms,self.vaspOUT.final_coords):
			print "*- Cluster Exploded! -*"
			self.genRandom()
		else:
			self.updatePool()

	def updatePool(self):

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		db.check()
		db.lock()

		self.readPool()

		energy = self.vaspOUT.final_energy
		finalXYZ = self.vaspOUT.final_coords

		finalXYZele = self.finalCoords(self.initialXYZ[2:],finalXYZ,self.vaspIN.box)

		self.poolList[self.strucNum:self.strucNum+self.stride-2] = finalXYZele
		self.poolList[self.strucNum-1] = "Finished Energy = " + str(energy) + "\n"

		self.writePool()

		db.unlock()

	def genRandom(self):

		db.check()
		db.lock()

		self.readPool()

		ranStruc = []
		r_ij = 3.0
		scale = self.natoms**(1./3.)

		for i in range(len(self.eleNames)):
			for j in range(self.eleNums[i]):
				x = ran.uniform(0,1) * self.r_ij * scale
				y = ran.uniform(0,1) * self.r_ij * scale
				z = ran.uniform(0,1) * self.r_ij * scale
				xyz = str(x) + " " + str(y) + " " + str(z) + "\n"
				xyzline = self.eleNames[i] + " " + xyz
				ranStruc.append(xyzline)

		self.poolList[self.strucNum:self.strucNum+self.stride-2] = ranStruc
		self.poolList[self.strucNum-1] = "NotMinimised Restart" + "\n"

		self.writePool()
		db.unlock()

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

		finalXYZele = CoM(finalXYZele,self.eleNames,self.eleMasses)

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
