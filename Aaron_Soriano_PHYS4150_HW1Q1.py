#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import sys

def ball(h):

    g = 9.81 #m/s^2, acceletartion due to gravity on Earth
    t = np.sqrt(2 * h / g) #s, time for ball to drop 
    
    print(f"The ball takes about {t:.3}s to drop from the top.")
    
    
if __name__ == "__main__":    
    h = float(sys.argv[1])
    ball(h)  
    