'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
The Johnston Group

20/3/15

--- Random Structure Minimiser Class ---

'''

import sys, os
import random as ran
import Database as db

from fixOverlap import fixOverlap
from DFT_input import vasp_input as DFTin
from DFT_output import vasp_output as DFTout
from checkPool import checkPool as checkPool
from CoM import CoM 
from Explode import checkClus

from SurfOpt import SurfOpt 
from surfacePOSCAR import surfacePOSCAR 

class minRan:

	def __init__(self
				,natoms,r_ij
				,eleNums,eleNames
				,eleMasses,nPool
				,stride,subString
				,boxAdd,surface
				,surfGA):

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

		db.lock()

		self.calcNum = db.findLastDir() + 1 
		os.system("mkdir " + str(self.calcNum))

		db.unlock()

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


		self.minimise()


	def minimise(self):

		'''
		Start 
		DFT calculation.
		'''

		if self.doDFT() == 0:

			output = DFTout(self.calcNum,self.natoms)

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
		os.chdir(base+"/"+str(self.calcNum))

		exitcode = os.system(self.subString)

		with open(base+"/exitcodes.dat","a") as exit:
			exit.write(str(self.calcNum))
			exit.write(" Exitcode = "+str(exitcode)+"\n")
			
		os.chdir(base)

		return exitcode

	def decide(self):

		'''
		Should cluster be added to pool.dat?
		'''

		if os.path.exists("pool.dat"):
			with open("pool.dat","r") as pool:
				poolList = pool.readlines()
				poolSize = len(poolList) / (self.natoms + 2)
				if poolSize < self.nPool:
					self.addToPool()
				else:
					AcceptReject = checkPool()
					Accept = AcceptReject.checkEnergy(float(self.finalEnergy))

					if Accept:
						Index = AcceptReject.lowestIndex
						Index = (Index*self.stride)+1

						db.updatePool("Finish"
									,Index,self.eleNums
									,self.eleNames,self.eleMasses
									,self.finalEnergy,self.finalCoords
									,self.stride,self.vaspIN.box)
		else:
			self.addToPool()


	def addToPool(self):

		'''
		Add Final Geometry and 
		energy to pool.dat.
		'''

		clus = []

		output = DFTout(self.calcNum,self.natoms)
		self.finalEnergy = output.getEnergy()
		self.finalCoords = output.getCoords()

		db.lock()

		with open("pool.dat","a") as pool:

			pool.write(str(self.natoms)+"\n")
			pool.write("Energy = "+str(self.finalEnergy))
			pool.write("   Dir = "+str(self.calcNum)+"\n")

			'''
			Move coordinates from 
			centre of the simulation cell.
			'''

			box = self.vaspIN.box
			self.finalCoords = [float(i) - box/2 for i in self.finalCoords]

			'''
			Change format of 
			the coordinates.
			'''

			for i in range(0,self.natoms*3,3):

				x = self.finalCoords[i]
				y = self.finalCoords[i+1]
				z = self.finalCoords[i+2]

				clus.append([x,y,z])

			'''
			Add the element types
			and write to pool file.
			'''

			count = 0

			for i in range(len(self.eleNames)):
				for j in range(self.eleNums[i]):
					ele = self.eleNames[i]
					x,y,z = clus[count]
					atom = ele+" "+str(x)+" "+str(y)+" "+str(z)+"\n"
					pool.write(atom)
					count += 1

		db.unlock()

