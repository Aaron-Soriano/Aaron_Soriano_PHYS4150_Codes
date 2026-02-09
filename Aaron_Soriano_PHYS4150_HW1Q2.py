#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse

def spaceship(x, v):

    c = 3.0e8 #m/s, Speed of light

    #Time relative to earth
    t_earth = x / (v*c)  #years 

    #Time relative to ship 
    gamma = np.sqrt(1 - v**2)
    t_ship = t_earth / gamma

    return (t_earth, t_ship)

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("x",
                        type = float,
                        help = "Distance to planet in lightyears")
    parser.add_argument("v",
                        type = float,
                        help = "Velocity of the space ship as a fraction of the speed of light")    
    args = parser.parse_args()

    t_earth, t_ship = spaceship(args.x, args.v)

    print(f"""From the perspective from an observer on earth, it would take 
    {t_earth:.3} years for the space ship to reach the planet.
    From the perspective from an observer on the ship, it would take 
    {t_ship:.3} years for the space ship to reach the planet.""")

