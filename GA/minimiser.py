'''
Minimiser

Jack Davis

10/10/14
'''

import os
import DFT_input as DFTin
import DFT_output as DFTout
import DFT_submit as DFTsub

from Select import tournamentSelect as select
from Crossover import crossover as cross 
from checkPool import checkPool as checkPool

class minimiser:

	def __init__(self,natoms,n,hpc,mpitasks):
		
		self.n = n
		self.natoms = natoms
		self.mpitasks = mpitasks
		self.stride = natoms + 2
		self.hpc = hpc

		self.runJobs()

	def runJobs(self):

		for i in range(self.n):

			strucNum = 0
			
			self.checkDB
			self.lockDB
			self.readPool()
			self.unlockDB

			for line in self.poolList:		
				strucNum += 1
				if "NotMinimised" in line:
					self.minimisePool(strucNum)
					break

		while self.checkFinished() == False:
			pass
		
		for i in range(self.n,self.n+1000):

			self.checkDB
			self.lockDB

			calcNum = self.findLastDir() + 1

			self.findPair()

			newClus = cross(self.clus1,self.clus2,self.natoms)

			self.offspring = newClus.CutSplice()

			self.unlockDB

			self.minimiseOffspring(calcNum,self.offspring)

	def minimiseOffspring(self,strucNum,offspring):

		'''
		Write XYZ for 
		offspring.
		'''

		xyzNum = strucNum

		with open(str(xyzNum)+".xyz","w") as xyzFile:
			xyzFile.write(str(self.natoms) + "\n\n")
			for line in offspring:
				xyzFile.write(line)

		# Run DFT calc
		vaspIN = DFTin.vasp_input(xyzNum)
		run = DFTsub.submit(self.hpc,xyzNum,self.mpitasks)
		# run.archer(xyzNum,self.mpitasks)
		vaspOUT = DFTout.vasp_output(xyzNum,self.natoms)

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		self.checkDB
		self.lockDB

		self.readPool()

		energy = vaspOUT.final_energy

		AcceptReject = checkPool(energy)

		Accept = AcceptReject.checkEnergy()

		if Accept:
			Index = AcceptReject.lowestIndex
			# StrucNum previously line number from file.
			Index = Index * self.stride
			NewCoords = vaspOUT.final_coords
			OldCoords = self.poolList[Index:Index+self.stride]
			NewCoordsEle = self.finalCoords(OldCoords[2:],NewCoords,vaspIN.box)
			self.poolList[Index+2:Index+self.stride] = NewCoordsEle
			self.poolList[Index+1] = "Finished Energy = " + str(energy) + "\n"
			self.writePool()

		self.unlockDB

	def minimisePool(self,strucNum):

		stride = self.stride
		xyzNum = ((strucNum-1)/stride) + 1

		'''
		Grab structure 
		from pool.dat
		and write .xyz.
		'''

		self.checkDB
		self.lockDB
		
		initialXYZ = self.poolList[strucNum-2:strucNum+stride-2]
		
		self.unlockDB

		with open(str(xyzNum)+".xyz","w") as xyzFile:
			for line in initialXYZ:
				xyzFile.write(line)

		'''
		Write Running flag 
		to pool and start 
		DFT calculation.
		'''

		self.checkDB
		self.lockDB

		# Write Running flag to pool.dat
		self.readPool()
		self.poolList[strucNum-1] = "Running\n"
		self.writePool()

		self.unlockDB

		# Run DFT calc
		vaspIN = DFTin.vasp_input(xyzNum)
		run = DFTsub.submit(self.hpc,xyzNum,self.mpitasks)
		# run.archer(xyzNum,self.mpitasks)
		vaspOUT = DFTout.vasp_output(xyzNum,self.natoms)

		'''
		After completion take
		final energy and coords
		from OUTCAR and Update
		poolList
		'''

		self.checkDB
		self.lockDB

		self.readPool()

		# Write final energy to pool.dat
		energy = vaspOUT.final_energy
		# Write final structure(minus element types)
		finalXYZ = vaspOUT.final_coords
		# Get element types and debox
		finalXYZele = self.finalCoords(initialXYZ[2:],finalXYZ,vaspIN.box)
		# Update pool 
		self.poolList[strucNum:strucNum+stride-2] = finalXYZele
		self.poolList[strucNum-1] = "Finished Energy = " + str(energy) + "\n"
		self.writePool()

		self.unlockDB

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

		return finalXYZele

	def checkFinished(self):

		'''
		Checks if all initial
		geometries relaxed.
		'''

		with open("pool.dat","r") as pool:
			for line in pool:
				if "Running" in line:
					return False

		return True

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

		with open("lock.db","w") as lock:
			lock.write("locked")

	def unlockDB(self):

		os.system("rm lock.db")

	def checkDB(self):

		while os.path.exists("Lock.dat"):
			pass 
		else:
			print "closed"

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
