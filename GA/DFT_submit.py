#!/usr/bin/env python

'''
DFT submission class for Ligand Mover.

Jack Davis

14/9/2014
'''

import os

class submit:
  
  '''
  DFT calculation is submitted 
  based on loop num i
  '''
  
  def __init__(self,hpc,i,mpitasks):

    self.i = i
    self.hpc = hpc
    self.mpitasks = mpitasks

    self.start(hpc)

  def start(self,hpc):
    
    if hpc == "bluebear":
      self.bluebear(self.i)
    elif hpc == "archer":
      self.archer(self.i,self.mpitasks)
      
  def bluebear(self,i):

    '''
    Job Submission for 
    Bluebear 
    '''

    base = os.environ["PWD"]
    runString = "mpirun vasp"
    moduleString = "module load apps/vasp; "
    os.chdir(base + "/" + str(i))
    os.system(moduleString + runString)
    os.chdir(base)

  def archer(self,i,mpitasks):

    '''
    Job submission for 
    Archer
    ''' 

    print "*Submitting Job*"

    base = os.environ["PWD"]
    runString = "aprun -n {0} vasp5.gamma".format(mpitasks)
    moduleString = "source /etc/profile; module load vasp5; "
    subshellString =  "/bin/bash --login -c "
    os.chdir(os.environ["PBS_O_WORKDIR"])
    os.chdir(base + "/" + str(i))
    commandString = moduleString + runString
    os.system(subshellString + "'" + commandString + "'")
    os.chdir(base)
