'''
Database operations.

Jack Davis

5/11/2014
'''

import os

def lock():

	os.system("touch lock.db")

def unlock():

	os.system("rm lock.db")

def check():

	while os.path.exists("lock.db"):
		pass