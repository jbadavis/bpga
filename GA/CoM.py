'''
Minimiser

Jack Davis

10/10/14
'''

def CoM(clus,eleNames,eleMasses):

	Coords = [] 
	CoMCoords = []
	cx = 0
	cy = 0 
	cz = 0
	totmass = 0

	for i in range(len(eleNames)):
		for line in clus:
			ele,x,y,z = line.split()
			if ele == eleNames[i]:
				totmass += eleMasses[i]
				cx += eleMasses[i] * float(x)
				cy += eleMasses[i] * float(y)
				cz += eleMasses[i] * float(z)

	cx *= (1/totmass)
	cy *= (1/totmass)
	cz *= (1/totmass)

 	for line in clus:
		ele,x,y,z = line.split()
		x = float(x) - cx
		y = float(y) - cy
		z = float(z) - cz
		xyz = ele+" "+str(x)+" "+str(y)+" "+" "+str(z)+"\n"
		CoMCoords.append(xyz)

	return CoMCoords