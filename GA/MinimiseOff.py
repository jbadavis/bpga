''' 
Minimiser

Jack Davis

20/10/14
'''

import os

import Database as db

import DFT_output as DFTout
import DFT_submit as DFTsub

from DFT_input import vasp_input as DFTin

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 

from Explode import checkClus

class minOff: 

	def __init__(self,natoms,eleNums,eleNames
		,eleMasses,n,cross,stride,hpc,mpitasks):
		
		self.natoms = natoms
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.eleNums = eleNums
		self.n = n
		self.cross = cross
		self.stride = stride
		self.hpc = hpc
		self.mpitasks = mpitasks

		print self.cross

		self.runCalc()

	def runCalc(self):

		'''
		Start calculation
		making new 
		directory.
		'''

		db.check()
		db.lock()

		self.xyzNum = self.findLastDir() + 1

		while os.path.exists(str(self.xyzNum)): 
			self.xyzNum = self.findLastDir() + 1 

		os.system("mkdir " + str(self.xyzNum))

		self.findPair()
		self.produceOffspring()

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

		self.findPair()
		self.produceOffspring()

		self.vaspIN = DFTin(self.xyzNum,self.eleNames
					,self.eleMasses,self.eleNums)

		db.unlock()

		self.runDFT()

	def findPair(self):

		'''
		From tournamentSelect the
		exact positions of the 
		random clusters is found in 
		the pool.
		'''

		# Select random pair 
		selectPair = select(self.n)
		self.pair = selectPair.pair

		#Postions of pair in poollist
		c1 = self.pair[0] * self.stride
		c2 = self.pair[1] * self.stride

		self.readPool()

		self.clus1 = self.poolList[c1+2:c1+self.stride]
		self.clus2 = self.poolList[c2+2:c2+self.stride]

		self.poolPos = [c1,c2]

	def produceOffspring(self):

		noOverlap = True
		noExplode = True 

		while noOverlap:

			newClus = cross(self.clus1,self.clus2,self.natoms,self.pair)

			# self.offspring = newClus.CutSplice()

			if self.cross == "random":
				self.offspring = newClus.CutSpliceRandom()
			elif self.cross == "weighted":
				self.offspring = newClus.CutSpliceWeighted()

			check = checkClus(self.natoms,self.offspring)
			noExplode = check.exploded()
			noOverlap = check.overlap()

			self.findPair()

		with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			xyzFile.write(str(self.natoms) + "\n\n")
			for line in self.offspring:
				xyzFile.write(line)

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
			Index = AcceptReject.lowestIndex
			# StrucNum previously line number from file.
			Index = Index * self.stride
			NewCoords = self.vaspOUT.final_coords
			OldCoords = self.poolList[Index:Index+self.stride]

			NewCoordsEle = self.finalCoords(OldCoords[2:]
							,NewCoords,self.vaspIN.box)

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
	