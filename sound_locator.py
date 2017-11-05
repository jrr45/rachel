#!/usr/bin/python


#This is a function that finds the location of a source of new sound given a system of nodes. the inputs are a delta vector containing the arrival lag from the new point to all of the nodes and the coorindates of the nodes themselves. the output is the coordinates of the nodes. x_mat has dimensions (3,N) where N is the number of nodes and d has dimensions (N,1). d should be shifted so that the smallest element is zero d=d-min(d). The over all shift factor will be fitted for.

#if the numbers look funny, this function is probably the problem


import numpy as np
import math
import scipy.optimize
import numpy.matlib
sqrt=math.sqrt	
fmin=scipy.optimize.fmin

def sound_finder(d,x_mat):

		
	
	#objective function
	def error(xguess,d,x_mat):
		y=x_mat.shape
		l=len(xguess)			
		x_matp=x_mat
		y=x_mat.shape
		K=xguess[1:l]
		K=numpy.matlib.repmat(K,7,1).T
		x_matp=x_mat-K
		delta=x_matp
		
		m=len(delta)
		
		J=sum((np.sqrt(sum(K**2))-(d+xguess[0]))**2)		


		print(J[0])
		return J[0]

	#make a guess
	xguess=np.random.randn(4,1)
	

	errorp= lambda x: error(x,d,x_mat)
	
 	#Final coordinates and shift
	xfin=fmin(errorp,xguess)
	
	#new coordinates
	new_coors=xfin[1:3]

	return new_coors


