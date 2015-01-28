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
from DFT_submit import submit as DFTsub

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 

from Explode import checkClus

class minPool:

	def __init__(self,natoms,r_ij
		,eleNums,eleNames
		,eleMasses,n,stride
		,hpc,mpitasks
		,subString):
		
		self.natoms = natoms
		self.r_ij = r_ij
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.n = n
		self.stride = stride
		self.hpc = hpc
		self.mpitasks = mpitasks
		self.subString = subString

		self.runCalc()

	def runCalc(self):

		self.findStruc()

	def findStruc(self):

		self.strucNum = 0

		time.sleep(ran.uniform(0,2.0))
			
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

		exitcode = os.system(self.subString)

		if exitcode == 0:
			# Get Energy.
			# Get Coordinates.
			self.updatePool()
			pass
		else:
			self.genRandom()

	# 	self.vaspIN = DFTin(self.xyzNum,self.eleNames
	# 				,self.eleMasses,self.eleNums)

	# 	run = DFTsub(self.hpc,self.xyzNum,self.mpitasks)
	# 	self.vaspOUT = DFTout(self.xyzNum,self.natoms)

	# 	'''
	# 	Check for errors in DFT.
	# 	Check if cluster has exploded.
	# 	Update pool!
	# 	'''

	# 	check = checkClus(self.natoms,self.vaspOUT.final_coords)

	# 	if self.vaspOUT.error:
	# 		print "*- Error in VASP Calculation -*"
	# 		self.genRandom()
	# 	elif check.exploded():
	# 		print "*- Cluster Exploded! -*"
	# 		self.genRandom()
	# 	else:	
	# 		self.updatePool()

	def updatePool(self):

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		finalEn=self.vaspOUT.final_energy
		finalCoords=self.vaspOUT.final_coords

		db.updatePool("Finish"
			,self.strucNum,self.eleNums,
			self.eleNames,self.eleMasses
			,finalEn,finalCoords
			,self.stride,self.vaspIN.box)

	def genRandom(self):

		coords=[]
		scale=self.natoms**(1./3.)

		finalEn=self.vaspOUT.final_energy

		for i in range(self.natoms*3):
			coords.append(ran.uniform(0,1)*self.r_ij*scale) 

		db.updatePool("Restart"
			,self.strucNum,self.eleNums,
			self.eleNames,self.eleMasses
			,finalEn,coords,self.stride
			,self.vaspIN.box)
