#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import matplotlib.pyplot as plt 
import matplotlib.patches as patch
import matplotlib.animation as anime

def particle_motion(steps, rng):
    #steps: int, number of time steps to run the simulation
    #rng: numpy random number generator
    #Simulates the motion of a 2D particle undergoing Brownian Motion
    # within a 101x101 block grid, over a course of `steps` time steps, 
    # and records the position of the particle at each point 
    
    x_coords = []
    y_coords = []
    x_pos = 0
    y_pos = 0

    for _ in range(steps):
        
        x_coords.append(x_pos)
        y_coords.append(y_pos)
        
        #Pick a move
        x_move, y_move = rng.choice((
            (0,  1), #Move up
            (0, -1), #Move down
            (1,  0), #Move right
            (-1, 0)  #Move left
        ))

        #If the particle goes out of bounds, "bounce" it back in
        if x_pos + x_move < -50 or x_pos + x_move > 50:
            x_move *= -1
        elif y_pos + y_move < -50 or y_pos + y_move > 50:
            y_move *= -1
        
        #Move the particle 
        x_pos += x_move
        y_pos += y_move    
    
    return x_coords, y_coords

def particle_animation(x_coords, y_coords, show_path):
    #x_coords, y_coords: list of ints, x,y coordinates of the particle
    #  at each step in the chain
    #show_path: bool, show the path of the particle
    #Displayed the animated path of the particle 
    
    #This is here because bool("False") == True
    if show_path == "True":  
        show_path = True
    elif show_path == "False":
        show_path = False
    else:
        raise Exception("Please only use 'True' or 'False'")
    
    fig, ax = plt.subplots()

    ax.set_xlim((-50, 50))
    ax.set_ylim((-50, 50))
    ax.set_title("Brownian Motion Particle")
    
    if show_path: #Only show the path if asked for
        line = ax.plot(x_coords[0], y_coords[0],
                       color = "green",
                       zorder = 1)[0]
    
    particle = patch.Circle((0,0),
                            radius = 1,
                            facecolor = "blue",
                            zorder = 2)
    ax.add_patch(particle)
    

    def update(frame):
        x_pos = x_coords[frame]
        y_pos = y_coords[frame]

        particle.set_center((x_pos, y_pos)) #Move the particle
        
        if show_path:                       #Only show the path if asked for
            line.set_xdata(x_coords[:frame])
            line.set_ydata(y_coords[:frame])
    
            return particle, line 
        
        return particle

    ani = anime.FuncAnimation(fig = fig,
                              func = update,
                              interval = 20, 
                              frames = args.steps
                              )    

    plt.show()

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("show_path",
                        type = str,
                        help = "Show the previous steps as a line behind the particle",
                        nargs = "?",
                        default = "True")   
    parser.add_argument("steps",
                        type = int,
                        help = "Number of steps for the particle to take",
                        nargs = "?",
                        default = 1000000) 
    parser.add_argument("seed",
                        type = int,
                        help = "Seed of the random number generator",
                        nargs = "?",
                        default = None)
    args = parser.parse_args()

    #Get coords of moving particle
    rng = np.random.default_rng(seed = args.seed)
    x_coords, y_coords = particle_motion(args.steps, rng)
    #Animate it
    particle_animation(x_coords, y_coords, args.show_path) 

    