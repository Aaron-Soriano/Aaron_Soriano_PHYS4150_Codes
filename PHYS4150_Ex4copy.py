#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

def hubble_data():

    #Data and plot set up
    dist, vel = np.loadtxt("hubble1929_table1.dat", usecols = (1, 2), unpack = True)
     
    fig, ax = plt.subplots(2, 1)
    best_fit_plot, residual_plot = ax
    
    #Scatter plot of data
    best_fit_plot.scatter(dist, vel)
    best_fit_plot.set_xlabel("Distance to galaxy")
    best_fit_plot.set_ylabel("Velocty of galaxy")
    best_fit_plot.set_title("Velocity vs Distances of Nearby Galaxies")
    
    #Plotting best fit line
    fit_line = np.polyfit(dist, vel, 1)
    vel_pred = lambda d: fit_line[1] + fit_line[0] * d
    
    dist_coords = np.linspace(0, 2, 100)
    vel_coords = vel_pred(dist_coords)
    best_fit_plot.plot(dist_coords, vel_coords, color = "red")
    
    #Residual plot
    residual = vel_pred(dist) - vel
    residual_plot.scatter(dist, residual)
    residual_plot.set_xlabel("Distance to galaxy")
    residual_plot.set_ylabel("Residual")

    #Final plot
    plt.subplots_adjust(hspace = 0, wspace = 0)
    plt.show()
    
if __name__ == "__main__":    
    hubble_data()