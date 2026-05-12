#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import argparse
import matplotlib.pyplot as plt
import itertools as it  


def quantum_zeno_run(N, N_prime, ME, ideal, seed = None, base_case = True): 
    
    def rotate(state, theta): 
        #state: Density matrix of current state
        #theta: angle to rotate 
        #Rotates the on/off switch of the quantum state given in `state` by an angle of `theta`
        #Returns the resulting density matrix

        #Rotate switch
        C = np.cos(theta/2) 
        S = np.sin(theta/2) 

        #Final assembly
            
        R = np.block([    
            [np.eye(4),         np.zeros((4, 4)),       np.zeros((4, 4))     ], #Rotate the Off/On switch
            [np.zeros((4, 4)),  np.diag([C, 1, 1, 1]),  np.diag([-S, 1, 1, 1])], #by theta, but only to 
            [np.zeros((4, 4)),  np.diag([S, 1, 1, 1]),  np.diag([C, 1, 1, 1])]  #|00> state
        ])

        after_state = R @ state @ R.T
        after_state /= np.trace(after_state)
        return after_state
    
    def rotate_prime(state, theta):
        #state: Density matrix of current state
        #theta: angle to rotate 
        #Rotates the off/off' switch  by an angle of `theta`
        #Returns the resulting density matrix
        
        #Rotate switch
        C = np.cos(theta/2) 
        S = np.sin(theta/2) 

        #Final assembly
        R = np.block([    
            [np.diag([C, 1, 1, 1]),  np.diag([-S, 1, 1, 1]), np.zeros((4, 4))],
            [np.diag([S, 1, 1, 1]), np.diag([C, 1, 1, 1]), np.zeros((4, 4))], #Rotate the Off'/Off switch
            [np.zeros((4, 4)),       np.zeros((4, 4)),      np.eye(4)       ]  #by theta
        ]) 

        after_state = R @ state @ R.T
        after_state /= np.trace(after_state)
        return after_state
    
    def grover_alg(state, ME, ideal = True):
        #State: Density matrix of current state
        #ME: The element to be interogated 
        #ideal: bool, idealized grover's alg, just outuputs |On>|ME>
        #Applies Grover's alg to `state`
        #Returns the resulting density matrix
        
        if ideal:
            Q = np.eye(4)
            Q[ME, 0 ] = 1
            Q[ME, ME] = 0
    
        else: 
            #Only apply to |00> -> Turn only |00> to superposition af all states
            applier = np.array([
                [0.25, 0, 0, 0],
                [0.25, 0, 0, 0],
                [0.25, 0, 0, 0],
                [0.25, 0, 0, 0]
            ])

            #Diffusive operator
            diffuse = np.eye(4) - (1/2)*np.ones((4,4)) 

            #Oracle operator
            oracle = np.zeros((4,4))                   #Interogating `ME` -> 0 all other columns 
            oracle[ME, ME] = 1                         #Only look at `ME`th column
            oracle = np.eye(4) - 2*oracle              
        
            Q = -oracle @ diffuse
            Q = Q @ Q @ applier
            row_ME = Q[ME, :] 
            Q = np.eye(4)
            Q[ME, :] = row_ME

        #Final assembly
        final_block = np.block([ 
            [np.eye(4),       np.zeros((4,4)), np.zeros((4,4))],  
            [np.zeros((4,4)), np.eye(4),       np.zeros((4,4))],
            [np.zeros((4,4)), np.zeros((4,4)), Q              ]
        ])
        
        #Searching over 4 elements -> sqrt(4) applications
        after_state =  final_block @ state @ final_block.T   
             
        after_state /= np.trace(after_state)
        return after_state 
    
    def measure(state, rng):
        #state: Density matrix of current state
        #rng: A numpy random number generator 
        #Returns a string giving the state measured and the desity matrix for the new state
        #after measuring the output qubits
        
        states = ["|Off00>", "|01>", "|10>", "|11>",
                  "|On00>", "|01>", "|10>", "|11>"]
        
        probs = np.array([state[i, i] for i in range(4, 12)], float) #The diagonals correspond 
                                                                 #to probabilites of measuring 
                                                                 #each state 
        probs = np.abs(probs)
        probs /= np.sum(probs)
        measurment = rng.choice(states, p = probs) #Pick a state

        detectors = {         #Turn this into a detector reading
            "|Off00>"  : "d5",
            "|01>"  : "d2",
            "|10>"  : "d3", 
            "|11>"  : "d4", 
            "|On00>"   : "d1", 
        }

        #Measument matrix 
        measured_index = states.index(measurment) % 4 
        M_mini = np.zeros((4, 4))
        M_mini[measured_index, measured_index] = 1

        M = np.block([
            [np.eye(4),       np.zeros((4,4)), np.zeros((4,4))],
            [np.zeros((4,4)), M_mini,          np.zeros((4,4))],
            [np.zeros((4,4)), np.zeros((4,4)), M_mini         ]
        ])

        after_state = M @ state @ M.T
        after_state /= np.trace(after_state)

        return detectors[measurment], after_state

    #Setup
    inital_state = np.zeros((12, 12))#Density matrix of system, states listed like: 
                                     #[|Off'00>, |Off'01>, |Off'10>, |Off'11>,
                                     # |Off00>, |Off01>, |Off10>, |Off11>,
                                     # |On00>, |On01>, |On10>, |On11>] 
    inital_state[0, 0] = 1           #Start in the |Off'00> state

    rng = np.random.default_rng(seed)
    
    measured_detections = {
        "d1" : 0,
        "d2" : 0,
        "d3" : 0,
        "d4" : 0,
        "d5" : 0
    }

    #The actual process

    if base_case:

        current_state = inital_state.copy() #New qubit
        theta = np.pi / 2                   #Angle for |Off / On> switch
        theta_prime = np.pi                 #Angle for |Off' / Off> swtich 

        for _ in range(N_prime):           
        
            current_state = inital_state.copy()                      #New qubit
            current_state = rotate_prime(current_state, theta_prime) #Rotate |Off' / Off> swtich 

            for _ in range(2):
            
                current_state = rotate(current_state, theta)             #Rotate |Off / On> switch
                current_state = grover_alg(current_state, ME, ideal)     #Apply alg. to |On00>
                final_state, current_state = measure(current_state, rng) #Measure the output qubits
                measured_detections[final_state] += 1                    #Record the result

        return measured_detections
        

    else:

        current_state = inital_state.copy() #New qubit
        theta = np.pi / N                   #Angle for |Off / On> switch
        theta_prime = np.pi / N_prime       #Angle for |Off' / Off> swtich 
        probd1_coords = []                  #To keep track of successes over time

        for i in range(N_prime):           
            current_state = inital_state.copy()                      #New qubit
            current_state = rotate_prime(current_state, theta_prime) #Rotate |Off' / Off> swtich 

            for _ in range(N):
                
                current_state = rotate(current_state, theta)             #Rotate |Off / On> switch
                current_state = grover_alg(current_state, ME, ideal)     #Apply alg. to |On00>
                final_state, current_state = measure(current_state, rng) #Measure the output qubits
                measured_detections[final_state] += 1                    #Record the result

            if i % 2 == 0: 
                probd1 = measured_detections["d1"] / sum(measured_detections.values())
                probd1_coords.append(probd1)
                    

        return probd1_coords
    
def base_case_graph(N_prime):
    #Displays a bar chart that shows the simplified version of the machanism (just the subroutine) 

    fig, ax = plt.subplot_mosaic([
        [f"ideal_{i}" for i in range(4)],
        [f"real_{i}" for i in range(4)]
    ], layout = "tight")

    for ME, id in it.product(range(4), (True, False)):
        
        #To locate which graph were in
        graph_name = "ideal_" if id else "real_"
        graph_name += str(ME)
        
        #Fill out graph
        measurements = quantum_zeno_run(1, N_prime, ME,
                                        ideal = id,
                                        base_case = True) 
        names = list(measurements.keys())                    
        values = np.array(list(measurements.values()))
        values = values / sum(values)
        
        ax[graph_name].bar(names, values,
                color = ["red", "orange", "yellow", "blue", "purple"],
                label = [f"Detector {i}" for i in range(1,6)]
                )
        ax[graph_name].set_ylim((0, 1))
        ax[graph_name].set_yticks([0, 0.25, 0.50, 0.75, 1])
        ax[graph_name].grid(which = "major",
                       axis = "y")
        alg = "Ideal" if id else "Real"
        ax[graph_name].set_title(f"ME = {ME} \n Grover's Alg: " + alg)
    
    fig.suptitle("Probabilites of Detecting a Particle at the Detectors")
    #plt.show()

def cfc_graph(N, N_prime):
    
    #Getting prob. of hitting Detector 1 for each ME
    prob_d1 = {
        "ME0": [],
        "ME1": [],
        "ME2": [],
        "ME3": []
        }

    for ME in range(4):
        measurement_coords = quantum_zeno_run(N, N_prime, ME,
                                              ideal = True,
                                              base_case = False)
        prob_d1[f"ME{ME}"] = measurement_coords  
        

    #P(Success|ME = i) = P(D1 hit|ME = i) / (P(D1 hit|ME = i) + P(D1 hit|ME = 1))
    num_points = len(prob_d1["ME0"])
    fig2, succ_plot = plt.subplots()

    for ME in range(4):
        for i in range(num_points):
            prob_d1_MEi = prob_d1[f"ME{ME}"][i]
            prob_d1_ME0 = prob_d1["ME0"][i]

            if (prob_d1_MEi + prob_d1_ME0) > 0:
                prob_d1[f"ME{ME}"][i] = prob_d1_MEi / (prob_d1_MEi + prob_d1_ME0)

        succ_plot.plot(range(num_points), prob_d1[f"ME{ME}"],
                 label = f"ME{ME}")
        succ_plot.set_title("Probability of Successful Interogation for each ME")
        #succ_plot.set_ylim((0, 1))

    
    fig2.legend()
    
        
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    parser.add_argument("N",
                        type = int,
                        help = "Number of subroutine divisions",
                        nargs = "?",
                        default = 2)
    parser.add_argument("N_prime",
                        type = int,
                        help = "Number of routine divisions",
                        nargs = "?",
                        default = 100)    
    args = parser.parse_args()

    #base_case_graph(args.N_prime)
    cfc_graph(args.N, args.N_prime)
    plt.show()
        
    
