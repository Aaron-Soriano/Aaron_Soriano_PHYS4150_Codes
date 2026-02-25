#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import ones,copy,cos,tan,pi
import numpy as np
import argparse 
import scipy.constants as c
import astropy.units as u

#Gaussian Quadriture code from Computational Physics, 2nd edition, by M. Newman
def gaussxw(N):

    # Initial approximation to roots of the Legendre polynomial
    a = np.linspace(3,4*N-1,N)/(4*N+2)
    x = cos(pi*a+1/(8*N*N*tan(a)))

    # Find roots using Newton's method
    epsilon = 1e-15
    delta = 1.0
    while delta>epsilon:
        p0 = ones(N,float)
        p1 = copy(x)
        for k in range(1,N):
            p0,p1 = p1,((2*k+1)*x*p1-k*p0)/(k+1)
        dp = (N+1)*(p0-x*p1)/(1-x*x)
        dx = p1/dp
        x -= dx
        delta = max(abs(dx))

    # Calculate the weights
    w = 2*(N+1)*(N+1)/(N*N*(1-x*x)*dp*dp)

    return x,w

def gaussxwab(N,a,b):

    #Get intial points/weights
    x,w = gaussxw(N)

    #Rescale 
    x_rescale = 0.5*(b-a)*x + 0.5*(b+a)
    w_rescale = 0.5*(b-a)*w

    return x_rescale, w_rescale
    

def quadrature(f, a, b, N):

    x_coords, weights = gaussxwab(N, a, b)
    f_coords = f(x_coords)

    return sum(f_coords * weights)
    
def Stefan_Boltzmann_estimation(error_threshold):

    def f(z): 
        x = z / (1-z)              #Subsitution
        f = x**3 / (np.exp(x) - 1)  #Original f
        dz = 1 / (z-1) ** 2        #Change in differential
        return f * dz

    a = 0 #Boundary change from subsitution
    b = 1
    
    #Determining needed points
    N = 2
    estimate_n = 0
    estimate_2n = quadrature(f, a, b, N)
    error = estimate_2n - estimate_n

    while error > error_threshold:

        estimate_n = estimate_2n
        estimate_2n = quadrature(f, a, b, 2*N)

        error = abs(estimate_2n - estimate_n)
        N *= 2

    #Calculating W/T^4
    constant = (c.k ** 4) / (4 * c.pi**2 * c.c**2 * c.hbar**3)

    total_energy =  constant * quadrature(f, a, b, 2*N) 

    return total_energy


if __name__ == "__main__":  

    parser = argparse.ArgumentParser()
    parser.add_argument("error_threshold",
                        type = float,
                        help = "Desired error of esimation",
                        nargs = "?",
                        default = 1e-14)   
    args = parser.parse_args()

    estimate = Stefan_Boltzmann_estimation(args.error_threshold)
    print(f"""The Stefan-Boltzmann constant is about {estimate:.16f} (units)
          which is {abs(c.Stefan_Boltzmann - estimate):.4f} away from the current measured value""")

