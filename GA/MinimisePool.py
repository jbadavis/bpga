'''
Minimise Pool

Jack Davis

20/10/14
'''

import os
import time
import random as ran

import Database as db

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 

from Explode import checkClus

class minPool:

	def __init__(self,natoms,r_ij
		,eleNums,eleNames
		,eleMasses,n,stride
		,subString):
		
		self.natoms = natoms
		self.r_ij = r_ij
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.subString = subString

		ran.seed()

		self.findStruc()

	def findStruc(self):

		self.strucNum = 0

		time.sleep(ran.uniform(0.0,2.0))
			
		db.lock()

		self.poolList = db.readPool()

		for line in self.poolList:		
			
			self.xyzNum = (self.strucNum/self.stride)+1

			if os.path.exists(str(self.xyzNum)):
				time.sleep(0.5)
			
			if "NotMinimised" in line:

				self.poolList[self.strucNum] = "Running\n"

				os.system("mkdir "+str(self.xyzNum))

				db.writePool(self.poolList)
				db.unlock()

				self.getXYZ()
				self.minimise()
				break

			elif "Restart" in line:

				self.poolList[self.strucNum] = "Running\n"
				db.writePool(self.poolList)
				db.unlock()

				self.getXYZ()
				self.minimise()
				break

			self.strucNum += 1

		if os.path.exists("lock.db"): 
			db.unlock()

	def getXYZ(self):

		'''
		Grab structure 
		from pool.dat
		and write .xyz.
		'''

		strucNum=self.strucNum
		stride=self.stride
		
		initialXYZ = self.poolList[strucNum-1:strucNum+stride-1]
		
		with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			for line in initialXYZ:
				xyzFile.write(line)
	
	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		self.vaspIN = DFTin(self.xyzNum,self.eleNames
						,self.eleMasses,self.eleNums)

		if self.doDFT() == 0:

			output = DFTout(self.xyzNum,self.natoms)

			if DFTout.checkError:
				self.genRandom()
			else:
				self.finalEnergy = output.getEnergy()
				self.finalCoords = output.getCoords()

				check = checkClus(self.natoms,self.finalCoords)

				if check.exploded() == False:
					self.updatePool()
				else:
					self.genRandom()

	def doDFT(self):

		'''
		Change directory and 
		submit calculation.
		'''

		base = os.environ["PWD"]
		os.chdir(base+"/"+str(self.xyzNum))

		exitcode = os.system(self.subString)

		with open(base+"/exitcodes.dat","a") as exit:
			exit.write(str(self.xyzNum))
			exit.write(" Exitcode = "+str(exitcode)+"\n")
			
		os.chdir(base)

		return exitcode

	def updatePool(self):

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		db.updatePool("Finish"
			,self.strucNum,self.eleNums,
			self.eleNames,self.eleMasses
			,self.finalEnergy,self.finalCoords
			,self.stride,self.vaspIN.box)

	def genRandom(self):

		ranCoords=[]
		scale=self.natoms**(1./3.)

		for i in range(self.natoms*3):
			ranCoords.append(ran.uniform(0,1)*self.r_ij*scale) 

		db.updatePool("Restart"
			,self.strucNum,self.eleNums
			,self.eleNames,self.eleMasses
			,self.finalEnergy,ranCoords
			,self.stride,self.vaspIN.box)
