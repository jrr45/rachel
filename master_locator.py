#!/usr/bin/python

import wave
import time
import numpy as np
import pyaudio
import scipy
import point_locator 
import math


# This is a function that takes in the distances between points and gives the location of the points in some coordinate system. So the only input is a matrix D such that D(i,j) is the distance between points i and j. YOU SHOULD ORDER D being thoughtful that the first computer will be placed at the origin. the second computer on the x axis third in the xy plane and so on.
#
transpose=np.transpose;
locatex=point_locator.point_locator;
sqrt=math.sqrt

def locations(d_mat):

	
		#for debuggin purposes
#	d_mat=np.array([[ 0.        ,  1.        ,  1.        ,  1.        ,  1.73205081],
 #      [ 1.        ,  0.        ,  1.41421356,  1.41421356,  1.41421356],
  #     [ 1.        ,  1.41421356,  0.        ,  1.41421356,  1.41421356],
   #    [ 1.        ,  1.41421356,  1.41421356,  0.        ,  1.41421356],
    #   [ 1.73205081,  1.41421356,  1.41421356,  1.        ,  0.        ]]);


	#find the shape of the distance matrix
	y=d_mat.shape;
	w=y[0];#this is the total number of points we have
	
	#define matrix of zeros to store locations	
	x_mat=np.zeros([3,4])
	d=d_mat;
	
	Ct=(d[0,1]**2+d[0,2]**2-d[1,2]**2)/(2*d[0,1]*d[0,2]);
	Cd=(d[0,1]**2+d[0,3]**2-d[1,3]**2)/(2*d[0,1]*d[0,3]);
	Cg=(d[0,2]**2+d[0,3]**2-d[2,3]**2)/(2*d[0,2]*d[0,3]);
	St=sqrt(abs(1-Ct**2));
	

	xix=d[0,3]*Cd;
	xiy=(St*Cg+(Ct/St)*Ct*Cg-(Ct/St)*Cd)*d[0,3];
	xiz=sqrt(abs(d[0,3]**2-xix**2-xiy**2));
		
	

	#Dont define x1, its already zero
	x2=np.array([d_mat[0,1],0,0]).T; 
	x3=np.array([Ct*d[0,2],St*d[0,3],0]).T;
	x4=np.array([xix,xiy,xiz]).T;

	


	x_mat[:,1]=x_mat[:,1]+x2;
	x_mat[:,2]=x_mat[:,2]+x3;
	x_mat[:,3]=x_mat[:,3]+x4;


	
	
	
	for n in range(4,w):
	
		#find the distances from established lattice points to new point.
		d=d_mat[0:n,n];
		
		#locate point based on distances
		xn=locatex(x_mat,d);
		
		xn=xn.reshape(3,1)
		
		x_mat=np.append(x_mat,xn,axis=1);

	return x_mat;
		








