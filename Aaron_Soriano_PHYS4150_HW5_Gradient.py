#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import scipy.constants as c
import matplotlib.pyplot as plt
import itertools as it

def E_potential(rx, ry):
    #rx, ry: floats, x,y coords of point
    
    #Two charges, 10cm away from eachother
    #positive charge on the left, negative charge on right
    q_plus = (-0.05, 0)
    q_minus = (0.05, 0)

    dist_plus = np.sqrt((rx - q_plus[0])**2 + (ry - q_plus[1])**2)
    dist_minus = np.sqrt((rx - q_minus[0])**2 + (ry - q_minus[1])**2)

    E_plus = 1 / (4 * c.pi * c.epsilon_0 * dist_plus)
    E_minus = -1 / (4 * c.pi * c.epsilon_0 * dist_minus) 

    return E_plus + E_minus

def gradient(f, rx, ry, h = 1e-5):
    #f: function to take gradient of
    #rx, ry: floats, x,y coords of point
    #h: float, (optional)
    
    dfdx = (f(rx + (h/2), ry) - f(rx - (h/2), ry)) / h
    dfdy = (f(rx, ry + (h/2)) - f(rx, ry - (h/2))) / h
    
    return (dfdx, dfdy)

def potential_and_gradient_graph():
    x = np.linspace(-0.5, 0.5, 100)
    y = np.linspace(-0.5, 0.5, 100)
    
    #Electical potental calculation 
    x_coords, y_coords = np.meshgrid(x, y)
    p_coords = E_potential(x_coords, y_coords)
    
    #Electrical force calculation
    gradE_x, gradE_y = gradient(E_potential, x_coords, y_coords)
    norm_factors = np.hypot(gradE_x, gradE_y)

    #Plotting
    potential_plot = plt.contourf(x_coords, y_coords, p_coords)
    force_plot = plt.quiver(x_coords, y_coords,
               10 * gradE_x / norm_factors , 10 * gradE_y / norm_factors,
               norm_factors,
               cmap = "RdBu")
    plt.title("Electric Potential with Electric Field")
    potential_scale = plt.colorbar(potential_plot, location = "bottom")
    potential_scale.ax.set_xlabel("Electrical Potential" + r" $V$")
    force_scale = plt.colorbar(force_plot, location = "bottom")
    force_scale.ax.set_xlabel("Electrical Field" + r" $\frac{V}{m}$")
    plt.show()

if __name__ == "__main__":    
    #To do: Add argparse support
    #Maybe potential/force/both/seperate
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
                        default = "both")   
    args = parser.parse_args()
    
    potential_and_gradient_graph()
    

