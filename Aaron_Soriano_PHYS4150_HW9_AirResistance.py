#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go


def acceleration(t, r, v, m):
    #t: float, current time
    #r: numpy array shape (2,1), a vector of the x and y components of the position
    #v: numpy array shape (2,1), a vector of the x and y components of the velocity
    #m: float, mass of the cannonball
    #Computes the acceleration of a cannon ball with drag, at the given velocity 
    #Returns a vector of the x and y components of the acceleration 
    
    R = 8 * (1/100) #cm -> m, radius of cannonball
    C = 0.47        #Coeff. of Drag
    rho = 1.22      #kg / m^3, Density of Air 
    g = 9.81        #m / s^2, Accelration Due to Gravity on Earth

    big_const = -(np.pi * R**2 * rho * C) / (2 * m)
    mag_v = np.hypot(v[0], v[1])       #Magnitude of v = sqrt(vx^2 + vy^2)

    ax = big_const * v[0] * mag_v      #X component of acceleration 
    ay = -g + big_const * v[1] * mag_v  #Y component of acceleration 

    return np.array([ax, ay])

def RK4(f, h, r0, v0, m):
    #Computes an aproximate solution to d^2r/dt^2 = `f`(t,r), r(0) = `r0`, r'(0) = `v0`
    #at `h` sized time steps, until the y component of position goes below 0
    #Using a 4th order Runga-Kutta method 

    
    velo = lambda t, r, v: v  #dr/dt = v, helper function 

    t_coords = []
    r_coords = []

    t = 0
    r = r0
    v = v0

    iterations = 0       #Max iterations 
    while r[1] >= 0 and iterations < 10000:   
        
        t_coords.append(t)
        r_coords.append(r)
        
        #Computing changes in t
        t += h

        #Computing changes in v as dv/dt = f(t, r, v)
        k1v = h * f(t, r, v, m)
        k2v = h * f(t + h/2, r + k1v/2, v + k1v/2, m)
        k3v = h * f(t + h/2, r + k2v/2, v + k2v/2, m)
        k4v = h * f(t + h, r + k3v, v + k3v, m)

        #Computing changes in r as dr/dt = v     
        k1r = h * velo(t, r, v)
        k2r = h * velo(t + h/2, r + k1r/2, v + k1r/2)
        k3r = h * velo(t + h/2, r + k2r/2, v + k2r/2)
        k4r = h * velo(t + h, r + k3r, r + k3r)

        #Apply changes
        v = v + (k1v + 2*k2v + 2*k3v + k4v) / 6
        r = r + (k1r + 2*k2r + 2*k3r + k4r) / 6

        iterations += 1

    return t_coords, r_coords

def plot_trajectory():
    
    theta = 30 * np.pi / 180                            #degrees -> radians, inital angle of the cannon
    r0 = np.array([0, 0])                               #m, Start at ground level
    v0 = 100 * np.array([np.cos(theta), np.sin(theta)]) #m/s, Inital velocity of cannonball
    h = 0.01                                             #s, Size of time step

    t_coords, r_coords = RK4(acceleration, h, r0, v0, 1) 
    
    x_coords = [r[0] for r in r_coords]
    y_coords = [r[1] for r in r_coords]
    
    trajectory_df = pd.DataFrame({ #Will hold all the data
            "x_coords" : [],
            "y_coords" : [],
            "mass" : []
            }) 

    for m in range(1, 21): #Testing masses from 1kg to 20kg
        _, r_coords = RK4(acceleration, h, r0, v0, m) 
    
        x_coords = [r[0] for r in r_coords]
        y_coords = [r[1] for r in r_coords]

        current_df = pd.DataFrame({
            "x_coords" : x_coords,
            "y_coords" : y_coords,
            "mass" : f"{m} kg"
            })
        
        trajectory_df = pd.concat([trajectory_df, current_df],
                                  ignore_index = True)
    
    fig = px.line(trajectory_df, 
                  x = "x_coords", y = "y_coords",
                  color = "mass",
                  title = "Cannon Trajectories")

    fig.update_layout(
            xaxis =  dict(title = {"text" : "Distance (m)"}),
            yaxis =  dict(title = {"text" : "Height (m)"}),
            legend = dict(title_text = "Mass (kg)")
         )
                
    fig.show()
    
if __name__ == "__main__":    
    """parser = argparse.ArgumentParser()
    parser.add_argument("plot_num",
                        type = int,
                        help = """""",
                        nargs = "?",
                        default = 0,
                        choices = [0, 1, 2, 3])   
    args = parser.parse_args()"""
    plot_trajectory()

