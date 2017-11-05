#!/usr/bin/python


import wave
import time
import numpy as np
import pyaudio
import scipy
import math


# This is a function that computes the cost function for a point. That is the      squared error summed over all points. 
#
# X is the test location of a point, V is the matrix that has the locations of the lattice points as column vectors, D contains the distances from the test point to the lattie points as elements. D is organized as (Nx1).


def cost(X,V,D):
	
	ds=len(D)
	J=0;
	
	for i in range(0,ds):

		J+=(np.linalg.norm(X-V[:,i])-D[i])**2
	
	return J



