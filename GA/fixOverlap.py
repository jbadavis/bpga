'''
fixOverlap

Jack Davis

13/11/14
'''

import numpy as np

def fixOverlap(coords):

	overlaped = True

	while overlaped:

		for i in range(len(coords)):
			for j in range(len(coords)):

				x = coords[i][1] - coords[j][1]
				y = coords[i][2] - coords[j][2]
				z = coords[i][3] - coords[j][3]

				r=(np.sqrt((x**2)+(y**2)+(z**2)))

				if r < .9 and r != 0:
					
					diff = .9 - r
					coords[i][1] += diff
					coords[i][2] += diff
					coords[i][3] += diff
					break

		else:
			overlaped = False

	return coords