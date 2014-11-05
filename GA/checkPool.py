'''
Check Pool Class

Jack Davis

16/10/14
'''

class checkPool:

	def __init__(self):

		self.energies = []

		self.getEnergies()

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

	def checkEnergy(self,newEnergy):

		HighestEnergy = max(self.energies)
		self.lowestIndex = self.energies.index(HighestEnergy)

		if newEnergy < HighestEnergy:
			self.Index = self.energies.index(HighestEnergy)
			return True
		else:
			return False

	def Convergence(self):

		poolMin = min(self.energies)
		poolMax = max(self.energies)

		if poolMin - poolMax > -0.01:
			print "Calculation Converged"
			return True
		else:
			return False
