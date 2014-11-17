''' 
Minimiser

Jack Davis

20/10/14
'''

import os

import Database as db

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout
from DFT_submit import submit as DFTsub

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 

from Explode import checkClus

class minOff: 

	def __init__(self,natoms,eleNums
		,eleNames,eleMasses
		,n,cross,stride
		,hpc,mpitasks):
		
		self.natoms = natoms
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.eleNums = eleNums
		self.n = n
		self.cross = cross
		self.stride = stride
		self.hpc = hpc
		self.mpitasks = mpitasks
		
		self.runCalc()

	def runCalc(self):

		'''
		Start calculation
		making new 
		directory.
		'''

		db.check()
		db.lock()

		self.xyzNum = db.findLastDir() + 1

		while os.path.exists(str(self.xyzNum)): 
			self.xyzNum = db.findLastDir() + 1 

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

		self.vaspIN = DFTin(self.xyzNum
			,self.eleNames,self.eleMasses
			,self.eleNums)

		db.unlock()

		self.runDFT()

	def produceOffspring(self):

		noOverlap = True
		noExplode = True 

		while noOverlap:

			newClus = cross(self.clus1,self.clus2
				,self.natoms,self.pair)

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

		poolList = db.readPool()

		self.clus1 = poolList[c1+2:c1+self.stride]
		self.clus2 = poolList[c2+2:c2+self.stride]

		self.poolPos = [c1,c2]

	def runDFT(self):

		run = DFTsub(self.hpc,self.xyzNum,self.mpitasks)
		self.vaspOUT = DFTout(self.xyzNum,self.natoms)

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

		finalEn=self.vaspOUT.final_energy
		finalCoords=self.vaspOUT.final_coords

		AcceptReject = checkPool()
		Accept = AcceptReject.checkEnergy(float(finalEn))

		if Accept:
			Index = AcceptReject.lowestIndex
			Index = (Index*self.stride)+1

			db.updatePool("Finish"
				,Index,self.eleNums,
				self.eleNames,self.eleMasses
				,finalEn,finalCoords
				,self.stride,vaspIN.box)

