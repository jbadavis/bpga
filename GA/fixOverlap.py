'''
fixOverlap

Jack Davis

13/11/14
'''

import numpy as np

def fixOverlap(coords):

	overlaped = True

	while overlaped:
		for i in range(0,len(coords),3):
			for j in range(0,len(coords),3):
				x=coords[i]-coords[j]
				y=coords[i+1]-coords[j+1]
				z=coords[i+2]-coords[j+2]
				r=(np.sqrt((x**2)+(y**2)+(z**2)))
				if r < .9 and r != 0:
					diff = .9 - r
					coords[i] += diff
					coords[i+1] += diff
					coords[i+2] += diff
					break
		else:
			overlaped = False

	return coords

