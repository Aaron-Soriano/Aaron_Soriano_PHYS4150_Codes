#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys

def spaceship(x, v):

    c = 3.0e8 #m/s, Speed of light

    #Time relative to earth

    t_earth = x / (v*c)  #years 

    #Time relative to ship 

    gamma = np.sqrt(1 - v**2)
    t_ship = t_earth / gamma

if __name__ == "__main__":    
    pass  