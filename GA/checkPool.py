'''
Check Pool Class

Jack Davis

16/10/14
'''

class checkPool:

	def __init__(self,newEnergy):

		self.newEnergy = newEnergy
		self.energies = []

		self.getEnergies()
		self.checkEnergy()

	def getEnergies(self):

		'''
		Get final energies
		from pool.dat after
		convergence.
		'''

		with open("pool.dat","r") as pool:
		  for line in pool:
			if "Finished Energy" in line:
			  energyList = line.split()
			  self.energies.append(float(energyList[3]))

	def checkEnergy(self):

		HighestEnergy = max(self.energies)
		lowestIndex = self.energies.index(HighestEnergy)

		if HighestEnergy > self.newEnergy:
			self.Index = self.energies.index(HighestEnergy)
			return True
		else:
			return False