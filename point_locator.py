#!/usr/bin/python

import wave
import time
import numpy as np
import pyaudio
from scipy import optimize
import cost_function

randn=np.random.randn
cost=cost_function.cost
# This function finds the location of a point with respect to a given lattice.
# The given lattice should be at least 4 computers to avoid ambiguities.
#
# The inputs are a matrix V that has the locations of the lattice points as column # vectors, and a vector D that has the list of distances from the lattice points to # the new point.
#
# Using a least squares fitting, we will find the location of the new point.

def point_locator(V,D):
		
	#randomly guess initial point	
	#x_int=0.1*(2*randn(3)-1);
	x_int=[[1],[1],[1]]
	#Error tolerance
	x_tol=0.00001;
	
	#maximum number of iters
	maxiter=50

	#minimize the error
	costp= lambda y: cost(y,V,D)
	x_opt=optimize.fmin(costp,x_int); 	
	
	x_opt=x_opt
	return x_opt;

	








