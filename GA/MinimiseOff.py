''' 
Minimiser

Jack Davis

20/10/14
'''

import os

import DFT_input as DFTin
import DFT_output as DFTout
import DFT_submit as DFTsub

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 

class minOff: 

	def __init__(self,natoms,eleNames,eleMasses,n,stride,hpc,mpitasks):
	# def __init__(self,xyzNum,natoms,eleNames,eleMasses,n,stride,hpc,mpitasks):
		
		# self.xyzNum = xyzNum
		self.natoms = natoms
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.hpc = hpc
		self.mpitasks = mpitasks

		self.runCalc()

	def runCalc(self):

		self.checkDB()
		self.lockDB()

		xyzNum = self.findLastDir() + 1

		self.findPair()
		self.produceOffspring()

		self.unlockDB()

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
		pair = selectPair.pair

		#Postions of pair in poollist
		c1 = ((pair[0]-1)*self.stride)
		c2 = ((pair[1]-1)*self.stride)

		self.readPool()

		self.clus1 = self.poolList[c1+2:c1+self.stride]
		self.clus2 = self.poolList[c2+2:c2+self.stride]

		self.poolPos = [c1,c2]

	def produceOffspring(self):

		newClus = cross(self.clus1,self.clus2,self.natoms)
		self.offspring = newClus.CutSplice()

		with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			xyzFile.write(str(self.natoms) + "\n\n")
			for line in self.offspring:
				xyzFile.write(line)

	def runDFT(self):

		self.vaspIN = DFTin.vasp_input(self.xyzNum)
		run = DFTsub.submit(self.hpc,self.xyzNum,self.mpitasks)
		self.vaspOUT = DFTout.vasp_output(self.xyzNum,self.natoms)

		if self.vaspOUT.error:
			print "*- Error in VASP Calculation -*"
		else:
			self.updatePool()

	def updatePool(self):

		self.checkDB()
		self.lockDB()

		self.readPool()

		energy = self.vaspOUT.final_energy

		AcceptReject = checkPool()
		Accept = AcceptReject.checkEnergy(energy)

		if Accept:
			Index = AcceptReject.lowestIndex
			# StrucNum previously line number from file.
			Index = Index * self.stride
			NewCoords = self.vaspOUT.final_coords
			OldCoords = self.poolList[Index:Index+self.stride]
			NewCoordsEle = self.finalCoords(OldCoords[2:],NewCoords,self.vaspIN.box)
			self.poolList[Index+2:Index+self.stride] = NewCoordsEle
			self.poolList[Index+1] = "Finished Energy = " + str(energy) + "\n"
			self.writePool()

		self.unlockDB()

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

	def lockDB(self):

		os.system("touch lock.db")

		# with open("lock.db","w") as lock:
		# 	lock.write("locked")

	def unlockDB(self):

		os.system("rm lock.db")

	def checkDB(self):

		while os.path.exists("Lock.db"):
			pass 
	