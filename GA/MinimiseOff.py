'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

20/3/15

--- Offspring Minimiser ---

'''

import os

import Database as db

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout

from Crossover import crossover as cross 
from checkPool import checkPool as checkPool
from CoM import CoM 

from Explode import checkClus
from fixOverlap import fixOverlap

# Surface GA
from SurfOpt import SurfOpt 
from surfacePOSCAR import surfacePOSCAR 

# Testing
import sys


class minOff: 

	def __init__(self,natoms,eleNums
				,eleNames,eleMasses
				,nPool,cross,stride
				,subString
				,surface,surfGA):
		
		self.natoms = natoms
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.eleNums = eleNums
		self.nPool = nPool
		self.cross = cross
		self.stride = stride
		self.subString = subString

		'''
		Surface Object.
		'''

		self.surface = surface
		self.surfGA = surfGA

		''' --- ''' 
		
		self.runCalc()

	def runCalc(self):

		'''
		Start calculation
		making new 
		directory.
		'''

		db.lock()

		self.xyzNum = db.findLastDir() + 1

		while os.path.exists(str(self.xyzNum)): 
			self.xyzNum = db.findLastDir() + 1 

		os.system("mkdir " + str(self.xyzNum))

		# self.findPair()
		self.produceOffspring()

		db.unlock()

		self.minimise()

	def produceOffspring(self):

		'''
		Produces XYZ after 
		crossover. 
		'''

		newClus = cross(self.cross,self.nPool,self.stride
						,self.eleNums,self.eleNames,self.natoms)

		self.offspring = newClus.mate()

		self.offspring = fixOverlap(self.offspring)

		# if self.cross == "random":

		# 	if len(self.eleNames) >= 2:
		# 		self.offspring = newClus.randomBimetallic()
		# 	else:
		# 		self.offspring = newClus.CutSpliceRandom()

		# elif self.cross == "weighted":

		# 	if len(self.eleNames) >= 2:
		# 		self.offspring = newClus.weightedBimetallic()
		# 	else:
		# 		self.offspring = newClus.CutSpliceWeighted()

		# elif self.cross == "bimetallic":

		# 	self.offspring = newClus.CutSpliceBimetallic()

		if self.surfGA:

			self.offspring = CoM(self.offspring,self.eleNames,self.eleMasses)

			SurfaceStruc = SurfOpt(self.offspring,self.surface,self.eleNames)

			self.offspring = SurfaceStruc.placeClus()

			self.vaspIN = surfacePOSCAR(self.xyzNum,self.offspring
										,self.surface)

		else:

			# with open(str(self.xyzNum)+".xyz","w") as xyzFile:
			# 	xyzFile.write(str(self.natoms)+"\n")
			# 	xyzFile.write("Crossover"+"\n")
			# 	for atom in self.offspring:
			# 		ele,x,y,z = atom 
			# 		xyzLine = ele+" "+str(x)+" "+str(y)+" "+str(z)+"\n"
			# 		xyzFile.write(xyzLine)

			self.vaspIN = DFTin(self.xyzNum,self.offspring,self.eleNames
								,self.eleMasses,self.eleNums)

	def restart(self):

		'''
		Restart Calculation
		without making 
		new directory.
		'''

		db.lock()

		# self.findPair()
		self.produceOffspring()

		db.unlock()

		self.minimise()

	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		if self.doDFT() == 0:

			output = DFTout(self.xyzNum,self.natoms)

			if output.checkError():
				self.restart()
			else:
				self.finalEnergy = output.getEnergy()
				self.finalCoords = output.getCoords()

				check = checkClus(self.natoms,self.finalCoords)

				if check.exploded() == False:
					self.updatePool()
				else:
					self.restart()

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

		AcceptReject = checkPool()
		Accept = AcceptReject.checkEnergy(float(self.finalEnergy))

		if Accept:
			Index = AcceptReject.lowestIndex
			Index = (Index*self.stride)+1

			db.updatePool("Finish"
				,Index,self.eleNums,
				self.eleNames,self.eleMasses
				,self.finalEnergy,self.finalCoords
				,self.stride,self.vaspIN.box)

	# def findPair(self):

	# 	'''
	# 	From tournamentSelect the
	# 	exact positions of the 
	# 	random clusters is found in 
	# 	the pool.
	# 	'''

	# 	# Select random pair 
	# 	selectPair = select(self.nPool)
	# 	self.pair = selectPair.pair

	# 	#Postions of pair in poollist
	# 	c1 = self.pair[0] * self.stride
	# 	c2 = self.pair[1] * self.stride

	# 	poolList = db.readPool()

	# 	self.clus1 = poolList[c1+2:c1+self.stride]
	# 	self.clus2 = poolList[c2+2:c2+self.stride]

	# 	self.poolPos = [c1,c2]
