''' 
Minimise Mutant

Jack Davis

20/10/14
'''

import os
import random as ran

import Database as db

import DFT_output as DFTout
import DFT_submit as DFTsub

from DFT_input import vasp_input as DFTin

from checkPool import checkPool as checkPool
from CoM import CoM 

from Explode import checkClus

class minMut: 

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

		ran.seed()

		self.runCalc()

	def runCalc(self):

		db.check()
		db.lock()

		self.xyzNum = self.findLastDir() + 1

		self.randomXYZ()

		os.system("mkdir " + str(self.xyzNum))

		self.vaspIN = DFTin(self.xyzNum,self.eleNames
					,self.eleMasses,self.eleNums)
							
		db.unlock()

		self.runDFT()

	def restart(self):

		'''
		Restart Calculation
		without making 
		new directory.
		'''

		db.check()
		db.lock()

		self.randomXYZ()

		self.vaspIN = DFTin(self.xyzNum,self.eleNames
					,self.eleMasses,self.eleNums)

		db.unlock()

		self.runDFT()

	def randomXYZ(self):

		scale = self.natoms**(1./3.)

		coords = []

		noOverlap = True
		noExplode = True 	

		while noOverlap and noExplode:

			coords = []

			for i in range(self.natoms*3):
				coords.append(ran.uniform(0,1)*self.r_ij*scale)	

			check = checkClus(self.natoms,coords)

			noExplode = check.exploded()
			noOverlap = check.overlap()

		coords = [coords[i:i + 3] for i in range(0, len(coords), 3)]

		with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			c = 0
			xyzFile.write(str(self.natoms)+"\n")
			xyzFile.write("Mutant\n")
			for i in range(len(self.eleNames)):
				for j in range(self.eleNums[i]):
					xyz = coords[c]
					xyz = [str(k) for k in xyz]
					xyzLine = xyz[0]+" "+xyz[1]+" "+xyz[2]+"\n"
					xyzlineEle = self.eleNames[i] + " " + xyzLine
					xyzFile.write(xyzlineEle)
					c += 1

	def runDFT(self):

		run = DFTsub.submit(self.hpc,self.xyzNum,self.mpitasks)
		self.vaspOUT = DFTout.vasp_output(self.xyzNum,self.natoms)

		check = checkClus(self.natoms,self.vaspOUT.final_coords)

		if self.vaspOUT.error:

			print "*- Error in VASP Calculation -*"
			self.restart()

		elif check.exploded():

			print "*- Cluster Exploded! -*"
			self.restart()

		else:
			
			self.updatePool()

	def updatePool(self):

		db.check()
		db.lock()

		self.readPool()

		energy = float(self.vaspOUT.final_energy)

		AcceptReject = checkPool()
		Accept = AcceptReject.checkEnergy(energy)

		if Accept:
			print "Accepted"
			Index = AcceptReject.lowestIndex
			# StrucNum previously line number from file.
			Index = Index * self.stride
			NewCoords = self.vaspOUT.final_coords
			OldCoords = self.poolList[Index:Index+self.stride]
			NewCoordsEle = self.finalCoords(OldCoords[2:],NewCoords,self.vaspIN.box)
			self.poolList[Index+2:Index+self.stride] = NewCoordsEle
			self.poolList[Index+1] = "Finished Energy = " + str(energy) + "\n"
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

	def findLastDir(self):

		'''
		Finds directory
		containing last
		calculation.
		'''

		calcList = []
		dirList = os.listdir(".")

		for i in dirList:
			try:
				calcList.append(int(i))
			except ValueError:
				continue

		calcList = sorted(calcList)

		lastCalc = calcList[len(calcList)-1]

		return lastCalc

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
				
