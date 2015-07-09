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

--- Pool Minimiser Class ---

'''

import sys, os
import random as ran
from fixOverlap import fixOverlap

from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout
from checkPool import checkPool as checkPool
from CoM import CoM 
from Explode import checkClus

from SurfOpt import SurfOpt 
from surfacePOSCAR import surfacePOSCAR 

class minRan:

	def __init__(self,calcNum
				,natoms,r_ij
				,eleNums,eleNames
				,eleMasses,nPool
				,stride,subString
				,boxAdd,surface
				,surfGA):

		self.calcNum = calcNum
		self.natoms = natoms
		self.r_ij = r_ij
		self.eleNums = eleNums
		self.eleNames = eleNames
		self.eleMasses = eleMasses
		self.nPool = nPool
		self.stride = stride
		self.subString = subString
		self.boxAdd = boxAdd

		'''
		Surface Object.
		'''

		self.surface = surface
		self.surfGA = surfGA
		
		os.system("mkdir "+str(self.calcNum))

		self.genRan()

	def genRan(self): 

		clus = []
		scale=self.natoms**(1./3.)

		for i in range(len(self.eleNames)):
			for j in range(self.eleNums[i]):

				ele = self.eleNames[i]

				x = ran.uniform(0,1)*self.r_ij*scale
				y = ran.uniform(0,1)*self.r_ij*scale
				z = ran.uniform(0,1)*self.r_ij*scale

				atom = [ele,x,y,z]

				clus.append(atom)

		clus = fixOverlap(clus)

		if self.surfGA:

			'''
			Write Surface POSCAR.
			'''

			SurfaceStruc = SurfOpt(clus,self.surface,self.eleNames,self.eleMasses)
			surfClus = SurfaceStruc.placeClus()

			self.vaspIN = surfacePOSCAR(self.calcNum,self.eleNames,surfClus,self.surface)

		else: 

			'''
			Write gas-phase POSCAR.
			'''
	
			self.vaspIN = DFTin(self.calcNum,clus,self.eleNames
								,self.eleMasses,self.eleNums
								,self.boxAdd)


	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		if self.doDFT() == 0:

			output = DFTout(self.xyzNum,self.natoms)

			if output.checkError():
				self.genRan()
			else:
				self.finalEnergy = output.getEnergy()
				self.finalCoords = output.getCoords()

				check = checkClus(self.natoms,self.finalCoords)

				if check.exploded() == False:
					self.decide()
				else:
					self.genRan()

		else:

			self.genRan()

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

	def decide(self):

		'''
		Should cluster be added.
		'''

		with open("pool.dat","r") as pool:
			poolList = pool.readlines()
			poolSize = (len(poolList) - (2 * self.nPool)) / self.natoms 

		if poolSize == 0:

			with open("pool.dat","w") as pool:

				for atom in self.finalCoords:

					pool.write(atom)

		sys.exit()

















