#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import argparse
#import scipy.units as u
import scipy.constants as c

def bisection(f, guess_neg, guess_pos, error = 1e-15):
    #f: funtion to find the root of
    #guess_pos: float, the negative side of the guessed interval (left side)
    #guess_pos: float, the positve side of the guessed interval (right side)
    #error: float, width of the final interval

    interval = guess_pos - guess_neg

    iterations = 0 
    while (abs(2 * interval) >= error) and (iterations <= 100):
        
        interval = guess_pos - guess_neg
        guess_mid = guess_neg + interval/2 

        if f(guess_mid) > 0:
            guess_pos = guess_mid
        else:
            guess_neg = guess_mid 


        iterations += 1

    #Best guess for the root is at the middle of the current interval    
    
    return  guess_neg + interval/2 

def plot_energy_levels():
    
    w = 1e-9 #meters, width of potential well
    V = 20   #eV, depth of potential well 

    lhs = lambda E: np.tan(np.sqrt((w**2 * c.m_e * E) / (2 * c.hbar**2)))
    rhs_even = lambda E: np.sqrt((V - E) / E)
    rhs_odd = lambda E: -np.sqrt(E / (V - E))
    
    E_coords = np.arange(0, 20, 1)
    lhs_coords = lhs(E_coords)
    rhseven_coords = rhs_even(E_coords)
    rhsodd_coords = rhs_odd(E_coords)

    plt.plot(E_coords, lhs_coords, label = "Left side")
    plt.plot(E_coords, rhseven_coords, label = "Right side (even)")
    plt.plot(E_coords, rhsodd_coords, label = "Right side (odd)")
    plt.grid()
    plt.legend()
    plt.xlim((0, 20))

    plt.show()
    
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("plot_type",
                        type = str,
                        help = """Type of plot: 
                        potential: Electric potential
                        force: Electric field of plate
                        both: Both plots overlayed
                        seperate: Both plots, but seperate
                        """,
                        nargs = "?",
                        default = "both",
                        choices = ["potential", "force", "both", "seperate"])   
    args = parser.parse_args()

    plot_energy_levels()
    #To do: Show energy levels on graph
    