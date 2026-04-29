#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns   


def quantum_zeno_run(N, N_prime, ME, seed = None): 
    
    def rotate(state, theta): 
        #State: Density matrix of current state
        #theta: angle to rotate 
        #Rotates the on/off switch of the quantum state given in `state` by an angle of `theta`
        #Returns the resulting density matrix

        #Rotate switch
        """R = np.block([     
            [np.cos(theta/2) * np.eye(4), -np.sin(theta/2) * np.eye(4)], #Rotate the Off/On switch
            [np.sin(theta/2) * np.eye(4),  np.cos(theta/2) * np.eye(4)]  #by theta
        ]) """
        tl = np.zeros((4,4))
        tl[0,0] = np.cos(theta/2) 
        tr = np.zeros((4,4))
        tr[0,0] = -np.sin(theta/2) 
        bl = np.zeros((4,4))
        bl[0,0] = np.sin(theta/2) 
        br = np.zeros((4,4))
        br[0,0] = np.cos(theta/2)

        R = np.block([     
            [tl, tr], #Rotate the Off/On switch
            [bl, br]                #by theta
        ]) 

        after_state = R @ state @ R.T
        after_state /= np.trace(after_state)
        return after_state
    
    def grover_alg(state, ME):
        #State: Density matrix of current state
        #ME: The element to be interogated 
        #Applies Grover's alg to `state`
        #Returns the resulting density matrix

        diffuse = np.identity(4) - (1/2)*np.ones((4,4))          #Diffusive operator
        oracle = np.identity(4) - (1/2)*np.array([[1, 0, 0, 0],  #Oracle looks for |00>
                                                  [0, 0, 0, 0],
                                                  [0, 0, 0, 0],
                                                  [0, 0, 0, 0]])
        
        Q = np.block([
            [np.eye(4),         np.zeros((4,4))],  #Only apply the alg if swtich is |On>
            [np.zeros((4,4)), -diffuse @ oracle]
        ])
        
        after_state = Q @ Q @ state @ Q.T @ Q.T    #Searching over 4 elements -> sqrt(4) loops
        after_state /= np.trace(after_state)

        return after_state 
    
    def measure(state, rng):
        #state: Density matrix of current state
        #rng: A numpy random number generator 
        #Returns a string giving the state measured
        
        states = ["|Off00>", "|Off01>", "|Off10>", "|Off11>", "|On00>", "|On01>", "|On10>", "|On11>"]
        probs = [state[i, i] for i in range(8)] #The diagonals correspond to probabilites of
                                                #measuring each state                     
        measured_state = rng.choice(states, size = 1, p = probs)[0] #Pick a state
        
        detectors = {         #Turn this into a detector reading
            "|Off00>" : "d1",
            "|Off01>" : "d2",
            "|Off10>" : "d3", 
            "|Off11>" : "d4", 
            "|On00>"  : "d5", 
            "|On01>"  : "d2", 
            "|On10>"  : "d3", 
            "|On11>"  : "d4"
        }
        return detectors[measured_state]
    
    #Setup
    inital_state = np.array([ 
        [1, 0, 0, 0, 0, 0, 0, 0], #Density matrix of system, states listed like: 
        [0, 0, 0, 0, 0, 0, 0, 0], #[|Off00>, |Off01>, |Off10>, |Off11>, |On00>, |On01>, |On10>, |On11>]
        [0, 0, 0, 0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ], dtype = float)

    rng = np.random.default_rng(seed)
    
    measured_detections = {
        "d1" : 0,
        "d2" : 0,
        "d3" : 0,
        "d4" : 0,
        "d5" : 0
    }

    #The actual loop
    current_state = inital_state.copy()
    
    for j in range(N_prime):
        
        current_state = inital_state.copy()                    #New matrix
        theta = (j * np.pi) / (2 * N_prime)                    #Rotate |Off' / Off>
        current_state[0, 0] *= np.cos(theta) 

        for i in range(1, N+1):

            theta = (i * np.pi) / (2 * N)
            current_state = rotate(current_state, theta)       #Rotate switch
            current_state = grover_alg(current_state, ME)      #Apply alg. to |On00>
            current_state = rotate(current_state, theta)       #Rotate switch
            final_state = measure(current_state, rng)          #Look at detectors
            measured_detections[final_state] += 1              #Record the result
    
    return measured_detections

def measurement_graph(N, N_prime):
    #measurments: dict, constins the names of detectors and number of hits
    #Displays a bar chart that shows the  
    
    measurements_df = pd.DataFrame({})

    for ME in range(2):
        measurement = quantum_zeno_run(N, N_prime, ME)
        
    """names = list(measurements.keys())
    values = np.array(list(measurements.values()))
    values = values / sum(values)
    plt.bar(names, values,
            color = ["red", "orange", "yellow", "blue", "purple"],
            label = [f"Detector {i}" for i in range(1,6)]
            )
    
    plt.show()"""

if __name__ == "__main__":    
    """parser = argparse.ArgumentParser()
    parser.add_argument("x",
                        type = float,
                        help = "Distance to planet in lightyears")
    parser.add_argument("v",
                        type = float,
                        help = "Velocity of the spaceship as a fraction of the speed of light")    
    args = parser.parse_args()"""

    measurement_graph(1000, 1)
