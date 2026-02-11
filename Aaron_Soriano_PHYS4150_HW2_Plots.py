#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import matplotlib.pyplot as plt       

def deltoid_curve(N):

    theta = np.linspace(0, 2*np.pi, N)
    x_coords = 2 * np.cos(theta) + np.cos(2 * theta)
    y_coords = 2 * np.sin(theta) - np.sin(2 * theta)

    return (x_coords, y_coords)

def galilean_spiral(N):

    theta = np.linspace(0, 10*np.pi, N)
    r = theta ** 2
    x_coords = r * np.cos(theta)
    y_coords = r * np.sin(theta)

    return (x_coords, y_coords)

def fey_funtion(N):

    theta = np.linspace(0, 10*np.pi, N)
    r = (np.exp(np.cos(theta))) - (2*np.cos(4*theta)) + (np.sin(theta/12) ** 5)
    x_coords = r * np.cos(theta)
    y_coords = r * np.sin(theta)

    return (x_coords, y_coords)

def polar_plots(plot_num = 0):

    N = 1000
    plot_dict = {1:deltoid_curve,
                 2:galilean_spiral,
                 3:fey_funtion}
    plot_titles = {1:"Deltoid Curve",
                  2:"Galilean Spiral",
                  3:"Fey Funtion"}

    #Individual Plots
    if plot_num != 0:
        
        x_coords, y_coords = plot_dict[plot_num](N)
        plt.plot(x_coords, y_coords)
        plt.title(plot_titles[plot_num])
    
    #All 3 plots
    else:
        
        fig, axis = plt.subplots(1, 3)
        for i in range(1,4):

            ax = axis[i-1]
            x_coords, y_coords = plot_dict[i](N)
            ax.plot(x_coords, y_coords)
            ax.set_title(plot_titles[i])

    plt.show() 

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("plot_num",
                        type = int,
                        help = """Which plot to display, default all plots. 
                        1: Deltoid Curve 
                        2: Galilean Spiral 
                        3: Fey's Function""",
                        nargs = "?",
                        default = 0,
                        choices = [0, 1, 2, 3])   
    args = parser.parse_args()

    polar_plots(plot_num = args.plot_num)

    

    