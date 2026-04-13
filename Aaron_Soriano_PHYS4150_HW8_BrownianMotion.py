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

    fig, ax = plt.subplots()

    ax.set_xlim((-50, 50))
    ax.set_ylim((-50, 50))
    
    particle = patch.Circle((0,0),
                            radius = 1,
                            facecolor = "blue")
    ax.add_patch(particle)
    
    
    #line = patch.Polygon([(0, 0)],
    #                     closed = False,
    #                     fill = None,
    #                     edgecolor = 'green')
    #ax.add_patch(line)
    

    def update(frame):
        x_pos =  x_coords[frame]
        y_pos = y_coords[frame]

        particle.set_center = (x_pos, y_pos)
        #line.set_xy(x_coords[:frame], y_coords[:frame])
    
        return particle#, line 

    ani = anime.FuncAnimation(fig = fig,
                              func = update,
                              interval = 20, 
                              frames = args.steps
                              )    
    
    #if not show_path:  #Remove the path if not asked for
    #    line.remove()

    plt.show()

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("show_path",
                        type = bool,
                        help = "Show the previous steps as a line behind the particle",
                        nargs = "?",
                        default = False)   
    parser.add_argument("steps",
                        type = int,
                        help = "Numbper of steps for the particle to take",
                        nargs = "?",
                        default = 10) 
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

    