'''
Birmingham Parallel Genetic Algorithm

A pool genetic algorithm for the
structural characterisation of 
nanoalloys.

Please cite - 
A. Shayeghi et al, PCCP, 2015, 17, 2104-2112

Authors -
Jack Davis and the Johnston Group

10/10/14

--- Centre of Mass Function ---

'''

def CoM(clus,eleNames,eleMasses):

	Coords = [] 
	CoMCoords = []
	cx = 0
	cy = 0 
	cz = 0
	totmass = 0

	for i in range(len(eleNames)):
		for atom in clus:
			ele,x,y,z = atom
			if ele == eleNames[i]:
				totmass += eleMasses[i]
				cx += eleMasses[i] * x
				cy += eleMasses[i] * y
				cz += eleMasses[i] * z

	cx *= (1/totmass)
	cy *= (1/totmass)
	cz *= (1/totmass)

 	for i in range(len(clus)):
		ele,x,y,z = clus[i]
		x -= cx
		y -= cy
		z -= cz
		clus[i] = [ele,x,y,z]

	return clus