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

    E_plus = 1 * c.e / (4 * c.pi * c.epsilon_0 * dist_plus)
    E_minus = -1 * c.e / (4 * c.pi * c.epsilon_0 * dist_minus) 

    return E_plus + E_minus

def gradient(f, rx, ry, h = 1e-5):
    #f: function to take gradient of
    #rx, ry: floats, x,y coords of point
    #h: float, (optional)
    
    dfdx = (f(rx + (h/2), ry) - f(rx - (h/2), ry)) / h
    dfdy = (f(rx, ry + (h/2)) - f(rx, ry - (h/2))) / h
    
    return (-dfdx, -dfdy)

def potential_and_gradient_graph(plot_type):
    
    #Electical potental calculation 
    x = np.linspace(-0.5, 0.5, 100)
    y = np.linspace(-0.5, 0.5, 100)

    Ex_coords, Ey_coords = np.meshgrid(x, y)
    Ep_coords = E_potential(Ex_coords, Ey_coords)
    
    #Electrical force calculation
    x = np.linspace(-0.5, 0.5, 10)
    y = np.linspace(-0.5, 0.5, 10)

    gx_coords, gy_coords = np.meshgrid(x, y)
    gradE_x, gradE_y = gradient(E_potential, gx_coords, gy_coords)
    gradE_x *= -1 #Electric Field = -grad(potential)
    gradE_y *= -1
    norm_factors = np.hypot(gradE_x, gradE_y)

    #Plotting
    
    if plot_type == "potential":
        potential_plot = plt.contourf(Ex_coords, Ey_coords, Ep_coords)
        potential_scale = plt.colorbar(potential_plot, 
                                       location = "bottom")
        potential_scale.ax.set_xlabel("Electrical Potential" + r" $V$")
        plt.title("Electric Potential on the Plate")

    elif plot_type == "force":
        force_plot = plt.quiver(gx_coords, gy_coords,
                gradE_x / norm_factors, gradE_y / norm_factors,
                norm_factors,
                cmap = "RdBu")
        force_scale = plt.colorbar(force_plot,
                                   location = "bottom")
        force_scale.ax.set_xlabel("Electrical Field" + r" $\frac{V}{m}$")
        plt.title("Electric Field on the Plate")

    elif plot_type == "both":

        potential_plot = plt.contourf(Ex_coords, Ey_coords, Ep_coords)
        potential_scale = plt.colorbar(potential_plot,
                                       location = "bottom")
        potential_scale.ax.set_xlabel("Electrical Potential" + r" $V$")

        force_plot = plt.quiver(gx_coords, gy_coords,
                gradE_x / norm_factors , gradE_y / norm_factors, #Keep the vectors length 1
                norm_factors,                                    #Express magnitude in color
                cmap = "RdBu")
        force_scale = plt.colorbar(force_plot,
                                    location = "bottom")
        force_scale.ax.set_xlabel("Electrical Field" + r" $\frac{V}{m}$")
        plt.title("Electric Potential and Electric Field on the Plate")

    elif plot_type == "seperate":
        fig, (potential_axis, force_axis) = plt.subplots(1, 2)
        
        potential_plot = potential_axis.contourf(Ex_coords, Ey_coords, Ep_coords)
        potential_scale = fig.colorbar(potential_plot, location = "bottom")
        potential_scale.ax.set_xlabel("Electrical Potential" + r" $V$")
        potential_axis.set_title("Electric Potential")

        force_plot = force_axis.quiver(gx_coords, gy_coords,
                gradE_x / norm_factors , gradE_y / norm_factors, #Keep the vectors length 1
                norm_factors,                                    #Express magnitude in color
                cmap = "RdBu")
        force_scale = fig.colorbar(force_plot, location = "bottom")
        force_scale.ax.set_xlabel("Electrical Field" + r" $\frac{V}{m}$")
        force_axis.set_title("Electric Field")

        plt.suptitle("Electric Potential and Electric Field on the Plate")

    plt.tight_layout()
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
    
    potential_and_gradient_graph(args.plot_type)
    

